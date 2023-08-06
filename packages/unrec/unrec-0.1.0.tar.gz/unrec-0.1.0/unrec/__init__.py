
import sys
import pickle

# 内部での再帰呼び出し例外
class InnerRecCallException(Exception):
	def __init__(self, key):
		self.key = key

# 引数のkeyを生成
def gen_key(args, kwargs):
	key = pickle.dumps([args, kwargs])
	return key

# keyを元に戻す
def re_key(key):
	args, kwargs = pickle.loads(key)
	return args, kwargs

# 再帰をループにしたオブジェクト
class Unrec:
	# 初期化処理
	def __init__(self, original_func):
		# 元の関数
		self.org_func = original_func
		# 計算済みメモ
		self.memo = {}
		# 初回呼び出し
		self.initial_call = True
	# 関数の呼び出し
	def __call__(self, *args, **kwargs):
		# 引数のkeyを生成
		key = gen_key(args, kwargs)
		# メモの引き当て
		if key in self.memo: return self.memo[key]
		# 初回呼び出しの場合分岐
		if self.initial_call is True:
			# 初回呼び出しフラグをFalseに変更
			self.initial_call = False
			# loopで再帰を再現
			result = self.__rec_loop(initial_key = key)
			# 初回呼び出しフラグを戻す
			self.initial_call = True
			return result
		else:
			# 呼び出し深さをインクリメント
			self.depth += 1
			if self.depth >= 2: raise InnerRecCallException(key)
			result = self.org_func(*args, **kwargs)
			return result
	# loopで再帰を再現
	def __rec_loop(self, initial_key):
		# 未計算スタック
		self.key_stack = [initial_key]
		# ループ
		while True:
			try:
				if len(self.key_stack) == 0: break
				# 計算すべき内容を1つ取り出す
				key = self.key_stack[-1]
				# keyを元に戻す
				args, kwargs = re_key(key)
				# 呼び出して計算を試みる
				self.depth = 0	# 呼び出し深さ
				result = self(*args, **kwargs)
				# 計算結果を記録する
				self.memo[key] = result
				# スタックを一個減らす
				self.key_stack.pop()
			except InnerRecCallException as e:
				inner_key = e.key
				self.key_stack.append(inner_key)
		# 結果を返す
		return self.memo[initial_key]

# 再帰をループにするアノテーション
def unrec(original_func):
	# 再帰をループにしたオブジェクト
	post_obj = Unrec(original_func)
	return post_obj

# モジュールオブジェクトとmem関数を同一視
sys.modules[__name__] = unrec
