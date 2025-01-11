---

## Local-Setup

1. Use the specified Python version:
   ```bash
   3.12.7
   ```

2. Setup detectron2 inside the current repo:
   ```bash
   python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
   # (add --user if you don't have permission)
   
   # Or, to install it from a local clone:
   git clone https://github.com/facebookresearch/detectron2.git
   python -m pip install -e detectron2
   
   # On macOS, you may need to prepend the above commands with a few environment variables:
   CC=clang CXX=clang++ ARCHFLAGS="-arch x86_64" python -m pip install ...
   ```

3. Get your own ad image file and replace the current with the one of your choice. Kindly keep the same name:
   ```bash
   sample.jpeg
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python main.py
   ```

5. Final outputs can be seen inside processed directory
