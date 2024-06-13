
file=$(find . -maxdepth 1 -type f \( -name "*.cpp" -o -name "*.py" ! -name "run_tests.py" ! -name "test_generator.py"  \))
file=$(basename "$file")

if [[ "$file" == *.cpp ]]; then
    exe_file="a"
    if [ -f "$exe_file" ]; then
        ./"$exe_file"
    else
        echo "error: executable file '$exe_file' not found."
    fi
elif [[ "$file" == *.py ]]; then
    python3 "$file"
else
    echo "error: no .cpp or .py file found in the directory."
fi