import npyscreen
from . import Body, Person, Running, Database


GENERAL_INFO = ['Name', 'Age', 'Height', 'Weight',
                'Hormonal Sex', 'Waist', 'Hip']


class MainTui(npyscreen.ActionFormV2):

    def create(self):
        self.add(npyscreen.TitleFixedText,
                name='The Fitness App for Non-Binary People',
                value='[ Push Help Button to know more about]'
                )

        self.main_option = self.add(
            npyscreen.TitleSelectOne,
            values=['Quick', 'Create User', 'Update User'],
            name='Choose an option and continue with "Ok" '
            )

    def on_ok(self):
        #npyscreen.notify_confirm(f'{self.main_option.value[0]}')

        if self.main_option.value[0] == 0:
            self.parentApp.switchForm('Quick')

    def on_cancel(self):
        self.parentApp.switchForm(None)

class QuickTui(npyscreen.ActionFormV2):

    def create(self):
        self.add(npyscreen.TitleText, name='Get a quick overview')
        self.name = self.add(npyscreen.TitleText, name=GENERAL_INFO[0])
        self.age = self.add(npyscreen.TitleText, name=GENERAL_INFO[1])
        self.height = self.add(npyscreen.TitleText, name=GENERAL_INFO[2])
        self.weight = self.add(npyscreen.TitleText, name=GENERAL_INFO[3])
        self.horm_sex = self.add(npyscreen.TitleText, name=GENERAL_INFO[4])

    def on_ok(self):
        p = Person(self.name.value)
        b = Body(
            int(self.age.value),
            float(self.height.value),
            float(self.weight.value),
            self.horm_sex.value,
        )

        npyscreen.notify_confirm(p.__str__() + b.__str__(), wide=True)



    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class EnbyfitApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainTui, name='Enbyfit - Terminal App')
        self.addForm('Quick', QuickTui)


if __name__ == '__main__':

    npyscreen.wrapper(EnbyfitApp().run())
