import tkinter as tk
from ToolsByteScultor.ui_module import DataProcessorUI
from ToolsByteScultor.data_processor_module import DataProcessor

if __name__ == '__main__':
    root = tk.Tk()

    data_processor = DataProcessor()
    ui = DataProcessorUI(root, data_processor)

    root.mainloop()
