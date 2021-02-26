import sys
import os
import keyboard

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def clear_prev_lines(num_lines):
    for _ in range(num_lines):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def select_from_list(prompt, options):
    # the state object should keep track of the
    # selected options, cursor position, etc.
    class State:
        def __init__(self, prompt, options):
            self.cursor = 0
            self.selected = []
            self.prompt = prompt
            self.options = options
            self.show_menu(clear=False)

        def show_menu(self, clear=True):
            if clear:
                clear_prev_lines(len(self.options) + 1)

            print(
                self.prompt, '(Use ARROW_KEYS to navigate, press SPACE to select and ENTER to continue)')

            # show the options
            for i in range(len(self.options)):
                # if the cursor is on the option, use <
                arrow = '<' if self.cursor == i else ''
                # if the option is selected, use ☑︎, else use ◻︎
                check_box = '☑︎' if i in self.selected else '◻︎'
                print(check_box, self.options[i], arrow)

        def change_cursor(self, value):
            new_value = self.cursor + value
            # check if the new position would be in range
            if new_value < 0 or new_value >= len(self.options):
                return
            self.cursor += value
            self.show_menu()  # re-render the ui

        def toggle_selected(self):
            if self.cursor in self.selected:
                self.selected.remove(self.cursor)
            else:
                self.selected.append(self.cursor)
            self.show_menu()

        def show_end_menu(self):
            # to not show cursor, put the cursor on -1
            # which is not associated with any option
            self.cursor = -1
            self.show_menu()  # re-render the ui
            print()

    state = State(prompt, options)

    # set up the keybindings
    keyboard.add_hotkey('up', lambda: state.change_cursor(-1))
    keyboard.add_hotkey('down', lambda: state.change_cursor(1))
    keyboard.add_hotkey('space', lambda: state.toggle_selected())
    keyboard.add_hotkey('enter', lambda: state.show_end_menu())

    # do not go past this function until enter is pressed
    keyboard.wait('enter')

    # dispose all key bindings
    keyboard.unhook_all()
    # this fixes a weird bug that causes user input to be
    # executed in the terminal after the program halts
    input()
    sys.stdout.write(CURSOR_UP_ONE)

    # state.selected is a list of indexes where each index
    # refers to an element in the option array.
    return [options[selected] for selected in state.selected]


def get(prompt: str, getter):
    error = False
    while True:
        try:
            user_input = input(prompt)
            if error:
                clear_prev_lines(2)
                print(prompt + user_input)
            return getter(user_input)
        except:
            error = True
            clear_prev_lines(1)
            print(f'\"{user_input}\"',
                  "is not a valid input, please try again")

def get_float(prompt):
    return get(prompt, eval)


def get_variables(possible_variables: list) -> list:
    '''
    returns a list of tuples that corresponds with user input.
    for example:

        get_variables(['a', 'b', 'c'])

    may return:

        [('a', 0), ('b', 1), ('c', 2)]

    depending on user input
    '''

    variable_names = select_from_list(
        'What variables do you know?', possible_variables)

    if len(variable_names) == 0:
        print('You have to know at least one variable')
        return

    result = []
    for variable_name in variable_names:
        variable_value = get_float(variable_name + ' = ')
        result.append((variable_name, variable_value))
    return result

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{get_float("float: ")} is an awesome number 😸. Thank you.')
