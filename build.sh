#deactivate

python3 -m pip install --user --upgrade wheel
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
python3 setup.py sdist bdist_wheel
python3 -m twine upload --skip-existing --repository testpypi dist/*



#Prod
#python3 -m twine upload dist/*

#Install test
#python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps simple_ad