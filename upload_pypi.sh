#!/bin/zsh
###
 # @Author: wicsp wicspa@gmail.com
 # @Date: 2024-06-05 17:38:35
 # @LastEditors: wicsp wicspa@gmail.com
 # @LastEditTime: 2024-06-05 21:06:54
 # @FilePath: /wicspy/upload_pypi.sh
 # @Description: 
 # 
 # Copyright (c) 2024 by wicsp, All Rights Reserved. 
### 

rm -rf ./build
rm -rf ./dist
rm -rf ./wicspy.egg-info


python setup.py sdist bdist_wheel

python -m twine upload dist/*


git add . && git commit -m "update" && git push

