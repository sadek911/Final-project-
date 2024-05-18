
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
import subprocess

class FunctionInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Function code input area
        self.function_code_label = QLabel('Function Code:')
        self.function_code_input = QTextEdit()

        # Function name input field
        self.function_name_label = QLabel('Function Name:')
        self.function_name_input = QLineEdit()

        # Parameters input field
        self.params_label = QLabel('Parameters (comma-separated, e.g., a=5,b=10):')
        self.params_input = QLineEdit()

        # Project file selection
        self.project_file_label = QLabel('Select Project File:')
        self.project_file_button = QPushButton('Browse')
        self.project_file_button.clicked.connect(self.select_project_file)
        self.project_file_display = QLabel('No file selected')

        # Button to generate and run the code
        self.generate_button = QPushButton('Generate and Run')
        self.generate_button.clicked.connect(self.generate_and_run)

        # Output display area
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        # Add widgets to the layout
        self.layout.addWidget(self.function_code_label)
        self.layout.addWidget(self.function_code_input)
        self.layout.addWidget(self.function_name_label)
        self.layout.addWidget(self.function_name_input)
        self.layout.addWidget(self.params_label)
        self.layout.addWidget(self.params_input)
        self.layout.addWidget(self.project_file_label)
        self.layout.addWidget(self.project_file_button)
        self.layout.addWidget(self.project_file_display)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.output_display)

        self.setLayout(self.layout)

    def select_project_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Project File", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            self.project_file_display.setText(file_name)
            self.project_file_path = file_name

    def wrap_function_code(self, function_code, function_name, params):
        param_assignments = '\n'.join([f"{param.strip()} = {value.strip()}" for param, value in (p.split('=') for p in params.split(','))])
        call_code = f"""
if __name__ == "__main__":
    {param_assignments}
    result = {function_name}({', '.join(param.split('=')[0].strip() for param in params.split(','))})
    print(f"Result: {{result}}")
"""
        return function_code, call_code

    def generate_and_run(self):
        function_code = self.function_code_input.toPlainText()
        function_name = self.function_name_input.text()
        params = self.params_input.text()

        if not hasattr(self, 'project_file_path'):
            self.output_display.setText("Please select a project file.")
            return

        func_code, call_code = self.wrap_function_code(function_code, function_name, params)

        with open(self.project_file_path, 'r') as file:
            project_code = file.read()

        # Insert function and call code at the end of the project file
        updated_code = f"{project_code}\n\n{func_code}\n\n{call_code}"

        with open('temp_script.py', 'w') as file:
            file.write(updated_code)

        result = subprocess.run(['python', 'temp_script.py'], capture_output=True, text=True)
        self.output_display.setText(result.stdout)
