'''
1. import a.aa.module_AA 在使用时，必须加完整名称来引用，比如：a.aa.module_AA.fun_AA()
2. from a.aa import module_AA 在使用时，直接可以使用模块名。比如：module_AA.fun_AA()
3. from a.aa.module_AA import fun_AA 直接导入函数 在使用时，直接可以使用函数名。 比如：fun_AA()
'''
print('我是a包下aa子包里的AA模块')
name='shl'
def funA():
    print('funA')