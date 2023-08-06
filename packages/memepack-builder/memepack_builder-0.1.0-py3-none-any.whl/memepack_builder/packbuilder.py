__all__ = [
    'ERR_MISSING_ARGUMENT', 'ERR_MISMATCHED_FORMAT', 'WARN_IMPLICIT_FORMAT',
    'WARN_MODULE_NOT_FOUND', 'WARN_MOD_NOT_FOUND', 'WARN_KEY_NOT_FOUND',
    'WARN_MAPPING_NOT_FOUND', 'WARN_CORRUPTED_MAPPING', 'WARN_DUPLICATED_FILE',
    'WARN_UNKNOWN_MOD_FILE', 'PACK_LEGACY_FORMAT', 'PACK_CURRENT_FORMAT',
    'JEPackBuilder', 'BEPackBuilder'
]
import hashlib
import json
import os
from . import logger
from zipfile import ZipFile, ZIP_DEFLATED

ERR_OK = 0
ERR_MISSING_ARGUMENT = 100
ERR_MISMATCHED_FORMAT = 101

WARN_IMPLICIT_FORMAT = 200
WARN_MODULE_NOT_FOUND = 201
WARN_MOD_NOT_FOUND = 202
WARN_KEY_NOT_FOUND = 203
WARN_MAPPING_NOT_FOUND = 204
WARN_CORRUPTED_MAPPING = 205
WARN_DUPLICATED_FILE = 206
WARN_UNKNOWN_MOD_FILE = 207

PACK_LEGACY_FORMAT = 3
PACK_CURRENT_FORMAT = 7

keys = 'type', 'modules', 'mod', 'output', 'hash', 'compatible'


def _build_message(code: int, message: str):
    return {'code': code, 'message': message}


def _get_lang_filename(type: str) -> str:
    return type == 'normal' and 'zh_meme.json' or (
        type == 'compat' and 'zh_cn.json' or 'zh_cn.lang')


def _normalize_args(args: dict):
    return {k: args[k] for k in args if k in keys}


class pack_builder(object):
    '''
    Build packs.
    The builder accepts the building args, then build the packs on demand.
    '''

    def __init__(self, main_res_path: str, module_info: dict):
        self.__main_res_path = main_res_path
        self.__module_info = module_info
        self._logger = logger()
        self.clean_status()

    @property
    def build_args(self):
        return self.__build_args

    @build_args.setter
    def build_args(self, value: dict):
        self.__build_args = _normalize_args(value)

    @property
    def warning_count(self):
        return self._warning_count

    @property
    def error_code(self):
        return self._error_code

    @property
    def file_name(self):
        return self._file_name

    @property
    def main_resource_path(self):
        return self.__main_res_path

    @property
    def module_info(self):
        return self.__module_info

    @property
    def build_log(self):
        return self._logger.raw_log

    def clean_status(self):
        self._warning_count = 0
        self._error_code = ERR_OK
        self._logger.clear()
        self._file_name = ""

    def _raise_warning(self, msg: dict):
        entry = f"Warning [{msg['code']}]: {msg['message']}"
        self._logger.append(entry)
        self._warning_count += 1

    def _raise_error(self, msg: dict):
        entry = f"Error [{msg['code']}]: {msg['message']}"
        terminate_msg = "Terminate building because an error occurred."
        self._logger.append(entry)
        self._logger.append(terminate_msg)
        self._error_code = msg['code']

    def _parse_includes(self, type: str) -> list:
        includes = self.build_args['modules'][type]
        full_list = list(
            map(lambda item: item['name'], self.module_info['modules'][type]))
        if 'none' in includes:
            return []
        elif 'all' in includes:
            return full_list
        else:
            include_list = []
            for item in includes:
                if item in full_list:
                    include_list.append(item)
                else:
                    self._raise_warning(_build_message(
                        WARN_MODULE_NOT_FOUND, f'Module "{item}" does not exist, skipping.'))
            return include_list

    def _handle_modules(self, resource_list: list, language_list: list, mixed_list: list, collection_list: list):
        # get all resource, language and mixed modules supplied by collection
        collection_info = {
            k.pop('name'): k for k in self.module_info['modules']['collection']}
        for collection in collection_list:
            for module_type, module_list in (('language', language_list), ('resource', resource_list), ('mixed', mixed_list)):
                if module_type in collection_info[collection]['contains']:
                    module_list.extend(
                        collection_info[collection]['contains'][module_type])
        # mixed_modules go to resource and language, respectively
        resource_list.extend(mixed_list)
        language_list.extend(mixed_list)

    def _merge_language(self, main_lang_data: dict, lang_supp: list):
        lang_data = main_lang_data
        module_path = self.module_info['path']
        for item in lang_supp:
            add_file = os.path.join(module_path, item, "add.json")
            remove_file = os.path.join(module_path, item, "remove.json")
            if os.path.exists(add_file):
                lang_data |= json.load(open(add_file, 'r', encoding='utf8'))
            if os.path.exists(remove_file):
                for key in json.load(open(remove_file, 'r', encoding='utf8')):
                    if key in lang_data:
                        lang_data.pop(key)
                    else:
                        self._raise_warning(_build_message(
                            WARN_KEY_NOT_FOUND, f'Key "{key}" does not exist, skipping.'))
        return lang_data


class JEPackBuilder(pack_builder):
    def __init__(self, main_res_path: str, module_info: dict, mods_path: str, legacy_mapping_path: str):
        super().__init__(main_res_path, module_info)
        self.__mods_path = mods_path
        self.__legacy_mapping_path = legacy_mapping_path

    @property
    def mods_path(self):
        return self.__mods_path

    @property
    def legacy_mapping_path(self):
        return self.__legacy_mapping_path

    def build(self):
        self.clean_status()
        args = self.build_args
        # args validation
        result = self.__check_args()
        if result['code'] == ERR_OK:
            # process args
            # get language modules
            lang_supp = self._parse_includes("language")
            # get resource modules
            res_supp = self._parse_includes("resource")
            # get mixed modules
            mixed_supp = self._parse_includes("mixed")
            # get module collections
            module_collection = self._parse_includes("collection")
            # add modules to respective list
            self._handle_modules(res_supp, lang_supp,
                                 mixed_supp, module_collection)
            # get mods strings
            mod_supp = self.__parse_mods()
            # merge language supplement
            # TODO: split mod strings into namespaces
            main_lang_data = json.load(open(os.path.join(self.main_resource_path,
                                                         "assets/minecraft/lang/zh_meme.json"), 'r', encoding='utf8'))
            main_lang_data = self._merge_language(
                main_lang_data, lang_supp) | self.__get_mod_content(mod_supp)
            # get realms strings
            realms_lang_data = json.load(open(os.path.join(
                self.main_resource_path, "assets/realms/lang/zh_meme.json"), 'r', encoding='utf8'))
            # process pack name
            digest = hashlib.sha256(json.dumps(
                args).encode('utf8')).hexdigest()
            pack_name = args['hash'] and f"mcwzh-meme.{digest[:7]}.zip" or "mcwzh-meme.zip"
            self._file_name = pack_name
            # process mcmeta
            mcmeta = self.__process_meta(args)
            # decide language file name & ext
            lang_file_name = _get_lang_filename(args['type'])
            # set output dir
            pack_name = os.path.join(args['output'], pack_name)
            # mkdir
            if os.path.exists(args['output']) and not os.path.isdir(args['output']):
                os.remove(args['output'])
            if not os.path.exists(args['output']):
                os.mkdir(args['output'])
            # create pack
            info = f"Building pack {pack_name}"
            self._logger.append(info)
            pack = ZipFile(
                pack_name, 'w', compression=ZIP_DEFLATED, compresslevel=5)
            pack.write(os.path.join(self.main_resource_path,
                                    "pack.png"), arcname="pack.png")
            pack.write(os.path.join(self.main_resource_path,
                                    "LICENSE"), arcname="LICENSE")
            pack.writestr("pack.mcmeta", json.dumps(
                mcmeta, indent=4, ensure_ascii=False))
            # dump lang file into pack
            if args['type'] != 'legacy':
                # normal/compat
                pack.writestr(f"assets/minecraft/lang/{lang_file_name}",
                              json.dumps(main_lang_data, indent=4, ensure_ascii=True, sort_keys=True))
                pack.writestr(f"assets/realms/lang/{lang_file_name}",
                              json.dumps(realms_lang_data, indent=4, ensure_ascii=True, sort_keys=True))
            else:
                # legacy
                main_lang_data |= realms_lang_data
                legacy_content = self.__generate_legacy_content(main_lang_data)
                pack.writestr(
                    f"assets/minecraft/lang/{lang_file_name}", legacy_content)
            # dump resources
            self.__dump_resources(res_supp, pack)
            pack.close()
            self._logger.append(f"Successfully built {pack_name}.")
        else:
            self._raise_error(result)

    def __dump_resources(self, modules: list, pack: ZipFile):
        excluding = ('module_manifest.json', 'add.json', 'remove.json')
        module_path = self.module_info['path']
        for item in modules:
            base_folder = os.path.join(module_path, item)
            for root, _, files in os.walk(base_folder):
                for file in files:
                    if file not in excluding:
                        path = os.path.join(root, file)
                        arcpath = path[path.find(
                            base_folder) + len(base_folder) + 1:]
                        # prevent duplicates
                        if (testpath := arcpath.replace(os.sep, "/")) not in pack.namelist():
                            pack.write(os.path.join(
                                root, file), arcname=arcpath)
                        else:
                            self._raise_warning(_build_message(
                                WARN_DUPLICATED_FILE, f'Duplicated file "{testpath}", skipping.'))

    def __check_args(self):
        args = self.build_args
        # check essential arguments
        for key in ('type', 'modules', 'mod', 'output', 'hash'):
            if key not in args:
                return _build_message(ERR_MISSING_ARGUMENT, f'Missing required argument "{key}".')
        # check "format"
        if 'format' not in args or args['format'] is None:
            # did not specify "format", assume a value
            format = args['type'] == 'legacy' and PACK_LEGACY_FORMAT or PACK_CURRENT_FORMAT
            self._raise_warning(_build_message(
                WARN_IMPLICIT_FORMAT, f'Did not specify "pack_format". Assuming value is "{format}".'))
            args['format'] = format
        else:
            if (args['type'] == 'legacy' and args['format'] > 3) or (args['type'] in ('normal', 'compat') and args['format'] <= 3):
                return _build_message(ERR_MISMATCHED_FORMAT, f'Type "{args["type"]}" does not match pack_format {args["format"]}.')
        return _build_message(ERR_OK, 'Check passed.')

    def __process_meta(self, args: dict) -> dict:
        data = json.load(open(os.path.join(self.main_resource_path,
                                           'pack.mcmeta'), 'r', encoding='utf8'))
        pack_format = args['type'] == 'legacy' and PACK_LEGACY_FORMAT or (
            'format' in args and args['format'] or None)
        data['pack']['pack_format'] = pack_format or data['pack']['pack_format']
        if args['type'] == 'compat':
            data.pop('language')
        return data

    def __parse_mods(self) -> list:
        mods = self.build_args['mod']
        existing_mods = os.listdir(self.mods_path)
        if 'none' in mods:
            return []
        elif 'all' in mods:
            return existing_mods
        else:
            mods_list = []
            for item in mods:
                if item in existing_mods:
                    mods_list.append(item)
                elif (normed_path := os.path.basename(os.path.normpath(item))) in existing_mods:
                    mods_list.append(normed_path)
                else:
                    self._raise_warning(_build_message(
                        WARN_MOD_NOT_FOUND, f'Mod file "{item}" does not exist, skipping.'))
            return mods_list

    def __get_mod_content(self, mod_list: list) -> dict:
        mods = {}
        for file in mod_list:
            if file.endswith(".json"):
                mods |= json.load(
                    open(os.path.join(self.mods_path, file), 'r', encoding='utf8'))
            elif file.endswith(".lang"):
                with open(os.path.join(self.mods_path, file), 'r', encoding='utf8') as f:
                    mods |= (line.strip().split(
                        "=", 1) for line in f if line.strip() != '' and not line.startswith('#'))
            else:
                self._raise_warning(_build_message(
                    WARN_UNKNOWN_MOD_FILE, f'File type "{file[file.rfind(".") + 1:]}" is not supported, skipping.'))
        return mods

    def __generate_legacy_content(self, content: dict) -> str:
        # get mappings list
        mappings = json.load(open(os.path.join(self.legacy_mapping_path,
                                               "all_mappings"), 'r', encoding='utf8'))
        legacy_lang_data = {}
        for item in mappings:
            if (mapping_file := f"{item}.json") not in os.listdir(self.legacy_mapping_path):
                self._raise_warning(_build_message(
                    WARN_MAPPING_NOT_FOUND, f'Missing mapping "{mapping_file}", skipping.'))
            else:
                mapping = json.load(
                    open(os.path.join(self.legacy_mapping_path, mapping_file), 'r', encoding='utf8'))
                for k, v in mapping.items():
                    if v not in content:
                        self._raise_warning(_build_message(
                            WARN_CORRUPTED_MAPPING, f'In file "{mapping_file}": Corrupted key-value pair {{"{k}": "{v}"}}.'))
                    else:
                        legacy_lang_data[k] = content[v]
        return ''.join(f'{k}={v}\n' for k, v in legacy_lang_data.items())


class BEPackBuilder(pack_builder):
    def __init__(self, main_res_path: str, module_info: dict):
        super().__init__(main_res_path, module_info)

    def build(self):
        self.clean_status()
        args = self.build_args
        # args validation
        result = self.__check_args()
        if result['code'] == ERR_OK:
            # get language modules
            lang_supp = self._parse_includes('language')
            # get resource modules
            res_supp = self._parse_includes('resource')
            # get mixed modules
            mixed_supp = self._parse_includes('mixed')
            # get module collections
            module_collection = self._parse_includes('collection')
            # merge collection into resource list
            self._handle_modules(res_supp, lang_supp,
                                 mixed_supp, module_collection)
            # process pack name
            digest = hashlib.sha256(json.dumps(
                args).encode('utf8')).hexdigest()
            pack_name = args['hash'] and f"meme-resourcepack.{digest[:7]}.{args['type']}" or f"meme-resourcepack.{args['type']}"
            self._filename = pack_name
            # create pack
            info = f"Building pack {pack_name}"
            self._logger.append(info)
            # set output dir
            pack_name = os.path.join(args['output'], pack_name)
            # mkdir
            if os.path.exists(args['output']) and not os.path.isdir(args['output']):
                os.remove(args['output'])
            if not os.path.exists(args['output']):
                os.mkdir(args['output'])
            # all builds have these files
            pack = ZipFile(
                pack_name, 'w', compression=ZIP_DEFLATED, compresslevel=5)
            pack.write(os.path.join(self.main_resource_path,
                                    "LICENSE"), arcname="LICENSE")
            pack.write(os.path.join(self.main_resource_path, "pack_icon.png"),
                       arcname="pack_icon.png")
            pack.write(os.path.join(self.main_resource_path, "manifest.json"),
                       arcname="manifest.json")
            self.__dump_language_file(pack, lang_supp)
            pack.write(os.path.join(self.main_resource_path, "textures/map/map_background.png"),
                       arcname="textures/map/map_background.png")
            # dump resources
            item_texture, terrain_texture = self.__dump_resources(
                res_supp, pack)
            if item_texture:
                item_texture_content = self.__merge_json(item_texture, "item")
                pack.writestr("textures/item_texture.json",
                              json.dumps(item_texture_content, indent=4))
            if terrain_texture:
                terrain_texture_content = self.__merge_json(
                    terrain_texture, "terrain")
                pack.writestr("textures/terrain_texture.json",
                              json.dumps(terrain_texture_content, indent=4))
            pack.close()
            self._logger.append(f'Successfully built {pack_name}.')

        else:
            self._raise_error(result)

    def __check_args(self):
        for item in ('type', 'compatible', 'modules', 'output', 'hash'):
            if item not in self.build_args:
                return _build_message(ERR_MISSING_ARGUMENT, f'Missing required argument "{item}".')
        return _build_message(ERR_OK, 'Check passed.')

    def __merge_json(self, modules: list, type: str) -> dict:
        name = type == "item" and "item_texture.json" or "terrain_texture.json"
        result = {'texture_data': {}}
        for item in modules:
            texture_file = os.path.join(
                self.module_info['path'], item, "textures", name)
            content = json.load(open(texture_file, 'r', encoding='utf8'))
            result['texture_data'] |= content['texture_data']
        return result

    def __dump_resources(self, modules: list, pack: ZipFile):
        item_texture = []
        terrain_texture = []
        for item in modules:
            base_folder = os.path.join(self.module_info['path'], item)
            for root, _, files in os.walk(base_folder):
                for file in files:
                    if file != "module_manifest.json":
                        if file == "item_texture.json":
                            item_texture.append(item)
                        elif file == "terrain_texture.json":
                            terrain_texture.append(item)
                        else:
                            path = os.path.join(root, file)
                            arcpath = path[path.find(
                                base_folder) + len(base_folder) + 1:]
                            # prevent duplicates
                            if (testpath := arcpath.replace(os.sep, "/")) not in pack.namelist():
                                pack.write(os.path.join(
                                    root, file), arcname=arcpath)
                            else:
                                self._raise_warning(_build_message(
                                    WARN_DUPLICATED_FILE, f"Duplicated '{testpath}', skipping."))
        return item_texture, terrain_texture

    def __dump_language_file(self, pack: ZipFile, lang_supp: list):
        with open(os.path.join(self.main_resource_path, "texts/zh_ME.lang"), 'r', encoding='utf8') as f:
            lang_data = dict(line[:line.find('#') - 1].strip().split("=", 1)
                             for line in f if line.strip() != '' and not line.startswith('#'))
        lang_data = ''.join(f'{k}={v}\t#\n' for k, v in self._merge_language(
            lang_data, lang_supp).items())
        if self.build_args['compatible']:
            pack.writestr("texts/zh_CN.lang", lang_data)
        else:
            for file in os.listdir(os.path.join(self.main_resource_path, "texts")):
                if os.path.basename(file) != 'zh_ME.lang':
                    pack.write(os.path.join(self.main_resource_path, f"texts/{file}"),
                               arcname=f"texts/{file}")
            pack.writestr("texts/zh_ME.lang", lang_data)
