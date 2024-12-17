from typing import Callable, Dict, Type, get_origin, get_args, Any

# 引数の値を取得する処理
def get_value_from_args(arg_name: str, args, kwargs, index: int):
    """引数名から引数の値を取得する"""
    if arg_name in kwargs:
        return kwargs[arg_name]
    if index < len(args):
        return args[index]
    raise ValueError(f"引数 '{arg_name}' が関数に渡されていません。")

# 型のチェックを行う処理
def check_type(arg_name: str, value, expected_type: Type, parent_name: str = None) -> None:
    """引数の型が正しいかチェックする"""
    origin = get_origin(expected_type)
    if origin:
        check_generic_type(arg_name, value, origin, expected_type)
    else:
        check_simple_type(arg_name, value, expected_type, parent_name)

def check_generic_type(arg_name: str, value, origin, expected_type: Type):
    """ジェネリック型のチェック"""
    if not isinstance(value, origin):
        raise TypeError(f"引数 '{arg_name}' は '{origin.__name__}' 型でなければなりません。現在の型: {type(value).__name__}")
    args = get_args(expected_type)
    if args:
        for i, item in enumerate(value):
            check_type(f"{arg_name}[{i}]", item, args[0], parent_name=arg_name)

def check_simple_type(arg_name: str, value, expected_type: Type, parent_name: str) -> None:
    """単純型のチェック"""
    if not isinstance(value, expected_type):
        raise TypeError(f"{parent_name or ''}引数 '{arg_name}' は '{expected_type.__name__}' 型でなければなりません。現在の型: {type(value).__name__}")

# 引数の型検証を行う処理
def validate_types(args, kwargs, types: Dict[str, Type]) -> None:
    """引数の型検証を行う"""
    if not types:
        return
    for index, (arg_name, expected_type) in enumerate(types.items()):
        value = get_value_from_args(arg_name, args, kwargs, index)
        check_type(arg_name, value, expected_type)

# 型チェックを行うデコレータ
def type_check_decorator(types: Dict[str, Any]):
    """引数の型チェックを行うデコレータ"""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            bound_args = args[1:] if args else []

            # キーワード引数の型チェック
            check_keyword_args(types, kwargs)

            # 位置引数の型チェック
            check_position_args(types, bound_args)

            return func(*args, **kwargs)

        return wrapper
    return decorator

def check_keyword_args(types: Dict[str, Any], kwargs: Dict[str, Any]) -> None:
    """キーワード引数の型をチェック"""
    for arg_name, arg_value in kwargs.items():
        if arg_name in types:
            expected_type = types[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(f"引数 '{arg_name}' は '{expected_type.__name__}' 型でなければなりません。現在の型: {type(arg_value).__name__}")

def check_position_args(types: Dict[str, Any], bound_args: list) -> None:
    """位置引数の型をチェック"""
    for i, arg_value in enumerate(bound_args):
        arg_name = list(types.keys())[i]
        expected_type = types[arg_name]
        if not isinstance(arg_value, expected_type):
            raise TypeError(f"引数 '{arg_name}' は '{expected_type.__name__}' 型でなければなりません。現在の型: {type(arg_value).__name__}")
