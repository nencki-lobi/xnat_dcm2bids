### dcm2niix customization


1. Open **Anaconda Prompt** and start Python by typing:
    ```
   python
    ```

2. In the Python console, run the following commands to locate the `utils.py` file:

   ```python
   import dcm2bids.utils.utils
   print(dcm2bids.utils.utils.__file__)
   ```
    You will get a path similar to:

   ```
   /Users/bkossowski/Praca/xnat_dcm2bids/venv/lib/python3.13/site-packages/dcm2bids/utils/utils.py
   ```

4. Open the `utils.py` file in a text editor (e.g., Notepad, VS Code).

5. Find the following line:

   ```python
   dcm2niixOptions = "-b y -ba y -z y -f '%3s_%f_%p_%t'"
   ```

6. Change `-z y` to `-z n` so the line looks like this:

   ```python
   dcm2niixOptions = "-b y -ba y -z n -f '%3s_%f_%p_%t'"
   ```

This will disable compression in `dcm2niix` when using `dcm2bids`.


