#!/usr/bin/env python3

import os
import wx
import json
import time

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show()
        return True

import wx
import os
import json
import time

import wx
import os
import json
import time

import wx
import os
import json
import time

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Выберите пользователей для подключения', size=(500, 400))
        self.SetMinSize((500, 400))
        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        top_panel = wx.Panel(panel)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        settings_button = wx.Button(top_panel, label='⚙️', size=(30, 30))
        settings_button.Bind(wx.EVT_BUTTON, self.on_settings)
        top_sizer.Add(settings_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        password_label = wx.StaticText(top_panel, label='Пароль:')
        top_sizer.Add(password_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.password_input = wx.TextCtrl(top_panel, style=wx.TE_PASSWORD, size=(150, -1))
        self.password_input.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        top_sizer.Add(self.password_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        top_panel.SetSizer(top_sizer)
        sizer.Add(top_panel, 0, wx.EXPAND)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        select_all_button = wx.Button(panel, label='Выбрать всё')
        select_all_button.Bind(wx.EVT_BUTTON, self.on_select_all)
        button_sizer.Add(select_all_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        clear_selection_button = wx.Button(panel, label='Очистить выбор')
        clear_selection_button.Bind(wx.EVT_BUTTON, self.on_clear_selection)
        button_sizer.Add(clear_selection_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        sizer.Add(button_sizer, 0, wx.CENTER)

        self.user_checklist = wx.CheckListBox(panel)
        self.user_checklist.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)  # Привязка контекстного меню
# self.user_checklist.Bind(wx.EVT_LISTBOX, self.on_item_select)  # Выделение элемента при клике
        sizer.Add(self.user_checklist, 1, wx.ALL | wx.EXPAND, 5)

        submit_button = wx.Button(panel, label='Подтвердить')
        submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        sizer.Add(submit_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)

        self.load_users()
        self.load_previous_selection()

    def load_user_mappings(self):
        self.mappings_file = os.path.expanduser("~/.user_mappings.json")
        if os.path.exists(self.mappings_file):
            with open(self.mappings_file, 'r') as f:
                return json.load(f)
        return {}

    def load_users(self):
        current_user = os.getenv("USER")
        user_mappings = self.load_user_mappings()

        user_list = [user_mappings.get(user, user) for user in os.listdir("/home")
                     if user != current_user and user.isalnum()]
        user_list.sort()
        self.update_user_checklist(user_list)

    def update_user_checklist(self, user_list):
        self.user_checklist.Clear()
        self.user_checklist.AppendItems(user_list)

    def load_previous_selection(self):
        selection_file = os.path.expanduser("~/.hue_selected_users")
        if os.path.isfile(selection_file):
            with open(selection_file, 'r') as f:
                previous_selection = f.read().strip().split(',')
                for user in previous_selection:
                    index = self.user_checklist.FindString(user)
                    if index != wx.NOT_FOUND:
                        self.user_checklist.Check(index)

    def on_submit(self, event):
        password = self.password_input.GetValue()
        if not password:
            wx.MessageBox("Пароль не был введён!", "Ошибка", wx.OK | wx.ICON_ERROR)
            return

        selected_users = []
        for index in range(self.user_checklist.GetCount()):
            if self.user_checklist.IsChecked(index):
                selected_users.append(self.user_checklist.GetString(index))

        if not selected_users:
            wx.MessageBox("Не выбрано ни одного пользователя!", "Ошибка", wx.OK | wx.ICON_ERROR)
            return

        selection_file = os.path.expanduser("~/.hue_selected_users")
        with open(selection_file, 'w') as f:
            f.write(','.join(selected_users))

        user_priorities = self.load_user_priorities()
        selected_users.sort(
    key=lambda user: user_priorities.get(self.get_real_user(user), 1000), reverse=True)

        for user in selected_users:
            real_user = self.get_real_user(user)
            command = f'sshpass -p "{password}" ssh -XY "{real_user}@localhost" /home/user/Desktop/Telegram/Telegram &'
            time.sleep(1)
            print(f"Выполняем команду: {command}")
            os.system(command)

        self.Close()

    def load_user_priorities(self):
        priorities_file = os.path.expanduser("~/.user_priorities.json")
        if os.path.exists(priorities_file):
            with open(priorities_file, 'r') as f:
                return json.load(f)
        return {}

    def on_settings(self, event):
        settings_frame = SettingsFrame(self)
        settings_frame.ShowModal()
        settings_frame.Destroy()

    def on_select_all(self, event):
        for index in range(self.user_checklist.GetCount()):
            self.user_checklist.Check(index)

    def on_clear_selection(self, event):
        for index in range(self.user_checklist.GetCount()):
            self.user_checklist.Check(index, False)

    def get_real_user(self, code_name):
        user_mappings = self.load_user_mappings()
        real_user = next((user for user, code in user_mappings.items() if code == code_name), None)
        return real_user if real_user else code_name

    def on_key_down(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.on_submit(event)
        else:
            event.Skip()

    def on_context_menu(self, event):
        # Получаем координаты клика правой кнопкой мыши
        pos = event.GetPosition()

        # Преобразуем координаты в глобальные, чтобы меню отображалось правильно
        pos = self.user_checklist.ScreenToClient(pos)

        # Проверим, был ли кликнут элемент в списке
        selected_index = self.user_checklist.HitTest(pos)
        if selected_index != wx.NOT_FOUND:
            self.user_checklist.SetSelection(selected_index)  # Выделяем элемент

            # Создаем контекстное меню
            menu = wx.Menu()

            # Добавляем пункт меню "Открыть отдельно"
            open_item = menu.Append(wx.ID_ANY, "Открыть отдельно")
            self.Bind(wx.EVT_MENU, self.on_open_separately, open_item)

            # Смещаем позицию меню на 20 пикселей вниз
            pos.y += 80  # Сдвигаем меню вниз на 20 пикселей

            # Показываем контекстное меню
            self.PopupMenu(menu, pos)
            menu.Destroy()


    def on_open_separately(self, event):
        # Получаем выбранный элемент списка
        selected_index = self.user_checklist.GetSelection()
        if selected_index != wx.NOT_FOUND:
            user = self.user_checklist.GetString(selected_index)
            password = self.password_input.GetValue()
            if not password:
                wx.MessageBox("Пароль не был введён!", "Ошибка", wx.OK | wx.ICON_ERROR)
                return
            
            # Выполнение команды для выбранного пользователя
            real_user = self.get_real_user(user)
            command = f'sshpass -p "{password}" ssh -XY "{real_user}@localhost" /home/user/Desktop/Telegram/Telegram &'
            print(f"Выполняем команду для {user}: {command}")
            os.system(command)
        else:
            wx.MessageBox("Не выбран пользователь!", "Ошибка", wx.OK | wx.ICON_ERROR)
    





class SettingsFrame(wx.Dialog):  # Наследуем от wx.Dialog вместо wx.Frame
    def __init__(self, parent):
        super().__init__(parent, title='Настройки', size=(500, 350))  # Увеличиваем размер окна
        self.SetMinSize((500, 350))  # Увеличиваем минимальный размер

        self.parent = parent  # Сохраняем ссылку на родительский класс

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        top_panel = wx.Panel(panel)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        filter_label = wx.StaticText(top_panel, label='Фильтр:')
        top_sizer.Add(filter_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.filter_input = wx.TextCtrl(top_panel, size=(200, -1))
        self.filter_input.Bind(wx.EVT_TEXT, self.on_filter)
        top_sizer.Add(self.filter_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        top_panel.SetSizer(top_sizer)
        sizer.Add(top_panel, 0, wx.EXPAND)

        # Создаём таблицу пользователей с дополнительной колонкой для приоритета
        self.user_table = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.user_table.InsertColumn(0, 'Кодовое имя', width=200)
        self.user_table.InsertColumn(1, 'Пользователь', width=200)
        self.user_table.InsertColumn(2, 'Приоритет', width=100)

        self.load_user_mappings()
        self.populate_table()

        sizer.Add(self.user_table, 1, wx.EXPAND | wx.ALL, 5)

        save_button = wx.Button(panel, label='Сохранить изменения')
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        sizer.Add(save_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)

        # Обработчик двойного щелчка для редактирования
        self.user_table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_edit)


    def load_user_mappings(self):
        self.mappings_file = os.path.expanduser("~/.user_mappings.json")
        if os.path.exists(self.mappings_file):
            with open(self.mappings_file, 'r') as f:
                self.user_mappings = json.load(f)
        else:
            self.user_mappings = {}

    def load_user_priorities(self):
        priorities_file = os.path.expanduser("~/.user_priorities.json")
        if os.path.exists(priorities_file):
            with open(priorities_file, 'r') as f:
                return json.load(f)
        return {}

    def populate_table(self, filter_text=''):
        current_user = os.getenv("USER")

        all_users = sorted([user for user in os.listdir("/home") if user.isalnum() and user != current_user])

        self.user_table.DeleteAllItems()
        for user in all_users:
            code_name = self.user_mappings.get(user, user)
            priority = self.load_user_priorities().get(user, 1000)
            if filter_text.lower() in code_name.lower() or filter_text.lower() in user.lower():
                index = self.user_table.InsertItem(self.user_table.GetItemCount(), code_name)
                self.user_table.SetItem(index, 1, user)
                self.user_table.SetItem(index, 2, str(priority))

    def on_filter(self, event):
        filter_text = self.filter_input.GetValue()
        self.populate_table(filter_text)

    def on_edit(self, event):
        item_index = event.GetIndex()
        user = self.user_table.GetItem(item_index, 1).GetText()
        code_name = self.user_table.GetItem(item_index, 0).GetText()

        priority = self.load_user_priorities().get(user, 1000)  # Получаем текущий приоритет

        # Создаём диалог для редактирования
        dialog = wx.Dialog(self, title=f'Редактировать пользователя: {user}', size=(400, 250))
        dialog.SetMinSize((400, 250))

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Поле для ввода нового кодового имени
        code_name_label = wx.StaticText(dialog, label="Кодовое имя:")
        sizer.Add(code_name_label, 0, wx.ALL, 5)
        code_name_input = wx.TextCtrl(dialog, value=code_name)
        sizer.Add(code_name_input, 0, wx.ALL | wx.EXPAND, 5)

        # Поле для ввода приоритета
        priority_label = wx.StaticText(dialog, label="Приоритет (чем выше, тем раньше запуск):")
        sizer.Add(priority_label, 0, wx.ALL, 5)
        priority_input = wx.TextCtrl(dialog, value=str(priority))
        sizer.Add(priority_input, 0, wx.ALL | wx.EXPAND, 5)

        # Кнопки "Сохранить" и "Отменить"
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(dialog, label="Сохранить")
        cancel_button = wx.Button(dialog, label="Отменить")
        button_sizer.Add(save_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER)

        dialog.SetSizer(sizer)

        # Устанавливаем фокус на поле для приоритета и выделяем весь текст
        priority_input.SetFocus()
        priority_input.SetSelection(0, len(priority_input.GetValue()))  # Выделяем весь текст

        # Обработка нажатия кнопок
        save_button.Bind(wx.EVT_BUTTON, lambda e: self.on_save_edit(e, dialog, user, code_name_input, priority_input))
        cancel_button.Bind(wx.EVT_BUTTON, lambda e: dialog.Close())

        dialog.ShowModal()


    def on_save_edit(self, event, dialog, user, code_name_input, priority_input):
        new_code_name = code_name_input.GetValue()
        new_priority = priority_input.GetValue()

        # Проверка на валидность приоритета
        try:
            new_priority = int(new_priority)
        except ValueError:
            wx.MessageBox("Приоритет должен быть числом!", "Ошибка", wx.OK | wx.ICON_ERROR)
            return

        # Обновляем кодовое имя и приоритет
        self.user_mappings[user] = new_code_name
        priorities = self.load_user_priorities()
        priorities[user] = new_priority

        # Сохраняем изменения
        with open(os.path.expanduser("~/.user_mappings.json"), 'w') as f:
            json.dump(self.user_mappings, f, indent=4)

        with open(os.path.expanduser("~/.user_priorities.json"), 'w') as f:
            json.dump(priorities, f, indent=4)

        # Закрываем диалог
        dialog.Close()

        # Обновляем таблицу
        self.populate_table()

    def on_save(self, event):
        with open(self.mappings_file, 'w') as f:
            json.dump(self.user_mappings, f)
        wx.MessageBox("Изменения сохранены!", "Успех", wx.OK | wx.ICON_INFORMATION)

        # Обновляем список пользователей в родительском окне
        self.parent.load_users()  # Обновляем список пользователей в родительском окне
        
        # Восстанавливаем выбор чекбоксов
        self.parent.load_previous_selection()
        
if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()