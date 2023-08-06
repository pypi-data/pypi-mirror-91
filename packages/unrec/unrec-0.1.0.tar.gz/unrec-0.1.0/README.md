再帰呼び出しを全自動でloopに直すツールです。
関数呼び出しの深さが非常に深くなっても正常に実行できます。

This is a tool to fix recursive calls to loop in a fully automatic manner.
It can execute successfully even when the depth of the function call is very deep.

## How to use: 使用法
```python
# pip install unrec

import unrec

@unrec
def frac(n):
	if n == 0: return 1
	return n * frac(n-1)

print(frac(9999))	# -> NO ERROR!!
```

This description is under construction.
