from cryptography.fernet import Fernet



class Crypt:
    __currentContents = None
    __filePath = None

    @property
    def content(self):
        raise Exception('Access Denied')

    @content.setter
    def content(self, file):
        self.__currentContents = file[0]
        self.__filePath = file[1].name      # file[0] is cont


    def encrypt(self):
        # with open(self.__filePath, 'rb') as file:

        key = Fernet.generate_key()
        f = Fernet(key)

        encContents = f.encrypt(self.__currentContents.encode('utf-8'))
        self.__currentContents = encContents.decode()

        return encContents, key


    def decrypt(self, key):

        key = key.lstrip().rstrip()
        decContents = None
        with open(self.__filePath, 'r') as file:
            f = Fernet(key)

            decContents = f.decrypt(file.read().encode('utf-8'))
            self.__currentContents = decContents.decode()
            # print(decContents)

        return decContents, None


    def write_to_file(self):
        with open(self.__filePath, 'w') as file:
            file.write(self.__currentContents)


