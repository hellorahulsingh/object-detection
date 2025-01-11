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
3. Setup detectron2 models & weight files
   ```
   git clone https://github.com/facebookresearch/detectron2.git
   ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the app:
   ```bash
   python main.py
   ```

6. Provide the path of the image when prompted

7. Final outputs can be seen inside processed directory
