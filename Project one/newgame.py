""" Memory game """

# To do :

    #2. edit texture of the whites and the imagess
    #3. edit the sizes of the pictures and the whites
    #4. celebrate when all are matched.
    #4. center the hamemo
    #5. change the background of the game page


# imports the arcade library and random.
import arcade
import random
import time
import threading

# Global variables
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Game"
SQUARE_SIZE = 170
GAP = 50
PIC_X_OFFSET = 200
PIC_Y_OFFSET = 680
NAME_Y_OFFSET = 680
NAME_X_OFFSET = 850
PICS = ["pics/admissions.png", "pics/burke.png", "pics/career.png", "pics/chapel.png",
        "pics/ccj.png", "pics/commons.png", "pics/DMC.png", "pics/ellihu.png",
        "pics/health.png", "pics/kirkland.png", "pics/kkj.png", "pics/martin.png",
        "pics/sadove.png", "pics/science.png", "pics/wellin.png"]

NAMES = ["pics/siuda.png", "pics/library.png", "pics/bris.png", "pics/chap.png",
        "pics/cj.png", "pics/comm.png", "pics/days.png", "pics/ell.png",
        "pics/healthcen.png", "pics/krikcoll.png", "pics/kj.png", "pics/martinsway.png",
        "pics/sad.png", "pics/scie.png", "pics/well.png"]

class Game(arcade.Window):
    """ Class for the Game."""

    def __init__(self):
        """ The constructor method."""

        # Calls the parent class constructor of the library.
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Makes the background image.
        self.welcome_background = None

        # Makes the welcome text.
        self.welcome_text = None

        # The square objects.
        self.all_pic_squares = None
        self.all_name_squares = None


        # The pics.
        self.all_pics = None

        # The names.
        self.all_names = None

        # Tracking the squares.
        self.held_squares = None

        # clcik tracker.
        self.pic_clicked = False
        self.name_clicked = False
        self.two_squares = []
        self.c = None

        # Number of matched squares.
        self.matched = 0
        self.text = None
        self.congrats = None



    def setup(self):
        """ Welcomes the player."""

        # Makes the background.
        self.welcome_background = arcade.Sprite("pics/welcome.png", scale = 0.8,
                                  center_x = 700, center_y = 400)

        # Welcome text.
        arcade.set_background_color(arcade.color.WHITE)
        self.welcome_text = arcade.draw_text("HaMemo", 380, 300, arcade.color.BLUEBONNET, 170,
                            font_name = ('Times New Roman'))
        self.text = arcade.draw_text("Click the up arrow to start", 380, 300, arcade.color.BLUEBONNET, 25,
                    font_name = ('Times New Roman'))

        self.congrats = arcade.Sprite("pics/congrats.jpeg", scale = 0.27, center_x = 2000, center_y = 2000)

        # Pic squares.
        self.all_pic_squares = arcade.SpriteList()
        self.all_name_squares = arcade.SpriteList()

        # Pics and Names.
        self.all_pics = arcade.SpriteList()
        self.all_names = arcade.SpriteList()


    def make_squares(self):
        """ Makes the squares. """

        # Makes the pic squares.
        y_offset = PIC_Y_OFFSET
        for row in range(5):
            for col in range(3):
                square = Square(arcade.Window, row, col, PIC_X_OFFSET + (col * SQUARE_SIZE), y_offset, 1)
                self.all_pic_squares.append(square)
            y_offset -= (SQUARE_SIZE // 2) + GAP

        for id, square in enumerate(self.all_pic_squares):
            square.assgin_id(id)


    def make_name_squares(self):
        """ Makes the name squares. """

        # Makes the name squares.
        y_offset = NAME_Y_OFFSET
        for row in range(5):
            for col in range(3):
                square = Square(arcade.Window, row, col, NAME_X_OFFSET + (col * SQUARE_SIZE), y_offset, 2)
                self.all_name_squares.append(square)
            y_offset -= (SQUARE_SIZE // 2) + GAP

        for id, square in enumerate(self.all_name_squares):
            square.assgin_id(id)


    def make_pics(self):
        """ Makes the pic objects. """

        for id,pic in enumerate(PICS):
            picture = Pic(pic, id)
            self.all_pics.append(picture)

    def make_names(self):
        """ Makes the name objects. """

        for id,name in enumerate(NAMES):
            pic = Name(name, id)
            self.all_names.append(pic)


    def assign(self):
        """ Assigns the names and pics with their respective squares. """

        names = []
        pics = []
        pic_squares = []
        name_squares = []

        for name in self.all_names:
            names.append(name)

        for pic in self.all_pics:
            pics.append(pic)

        for square in self.all_pic_squares:
            pic_squares.append(square)

        for square in self.all_name_squares:
            name_squares.append(square)

        # Shuffles the items in the name and pic list.
        random.shuffle(names)
        random.shuffle(pics)


        # Creates a random match of a square with either a pic or a name.
        pic_assignment = list(zip(pic_squares, pics))
        name_assignment = list(zip(name_squares, names))

        # Changes the assignment of each square based on the match made.
        for pair in pic_assignment:
            pair[0].change_assignment(pair[1])

        for pair in name_assignment:
            pair[0].change_assignment(pair[1])

    def on_draw(self):
        """ Draws the screen. """

        # Clears the screen and starts to redraw.
        arcade.start_render()

        # Draws the welcome page.
        self.welcome_background.draw()
        self.welcome_text.draw()
        self.text.draw()

        # Draws the pic and name squares.
        self.all_pic_squares.draw()
        self.all_name_squares.draw()

        # Draws the pics and the names.
        self.all_pics.draw()
        self.all_names.draw()

        self.congrats.draw()


    def on_key_press(self, key, mod):
        """ When the up arrow is clicked the game starts."""

        if key == arcade.key.UP:
            self.welcome_text.change_x = 800
            self.welcome_text.change_y = 800
            self.text.change_x = 800
            self.text.change_y = 800

    def on_key_release(self, key, mod):
        """ Changes the screen when the up arrow is clicked."""

        if key == arcade.key.UP:
            self.welcome_text.change_x = 0
            self.welcome_text.change_y = 0
            self.text.change_x = 0
            self.text.change_y = 0
            self.make_squares()
            self.make_name_squares()
            self.make_pics()
            self.make_names()
            self.assign()

    def on_update(self, time):
        """ Updates the changes made on the objects."""

        # Updsates the welcome image and text.
        self.welcome_background.update()
        self.welcome_text.update()
        self.text.update()
        self.all_pics.update()
        self.all_names.update()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        if self.pic_clicked == False:
            # Gets the clicked square.
            clicked_pic = arcade.get_sprites_at_point((x, y), self.all_pic_squares)
            if clicked_pic:
                self.pic_clicked = True
                self.two_squares.append(clicked_pic[0])
                pic = clicked_pic[0].get_assignment()
                center = clicked_pic[0]._get_position()
                pic.set_position(center[0], center[1])


        if self.name_clicked == False:
            clicked_name = arcade.get_sprites_at_point((x,y), self.all_name_squares)
            if clicked_name:
                self.name_clicked = True
                self.two_squares.append(clicked_name[0])
                name = clicked_name[0].get_assignment()
                center = clicked_name[0]._get_position()
                name.set_position(center[0], center[1])
                self.c = threading.Timer(1, self.check)
                self.c.start()

    def check(self):
        """ Checks if two squares are touched consequently. """

        self.check_match()
        self.two_squares = []
        self.name_clicked = False
        self.pic_clicked = False

    def check_match(self):
        """ Checks if the two boxes clicked are a match. """

        pic_square = self.two_squares[0]
        name_square = self.two_squares[1]

        pic_id = pic_square.get_assignment().get_id()
        name_id = name_square.get_assignment().get_id()

        if pic_id == name_id:

            pic_square.set_position(2000, 2000)
            name_square.set_position(2000, 2000)
            pic_square.get_assignment().set_position(2000, 2000)
            name_square.get_assignment().set_position(2000, 2000)

            self.matched += 2
            self.check_game()

        else:
            pic_square.get_assignment().set_position(2000, 2000)
            name_square.get_assignment().set_position(2000, 2000)

    def check_game(self):
        """ Checks if the game is over. """

        if self.matched == 30:
            #Change the screen and celebrate.
            self.welcome_background.set_position(2000, 2000)
            self.congrats.set_position(700, 400)
            


class Square(arcade.Sprite):
    """ Class for the squares. """

    def __init__(self, window, row, col, x, y, batch):
        """ The constructor method. """

        self.window = window
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.batch = batch
        self.assigned_to = None
        self.id = None


        # Image to use for the box when face down.
        self.body = "pics/box.jpg"

        super().__init__(self.body, scale = 0.1, center_x = self.x, center_y = self.y)
        #calculate_hit_box = False


    def assgin_id(self, num):
        """ Assigns id for each square. (counted from top left to bottom rigth)"""

        self.id = num

    def get_id(self):
        """ Returns (row, col) of the square object. """

        return (self.id)

    def change_assignment(self, object):
        """ Changes the pic/ name a square is assigned to. """

        self.assigned_to = object

    def get_assignment(self):
        """ Returns the onject assigned to a suare. """

        return self.assigned_to

class Pic(arcade.Sprite):
    """ Class for the pictures. """

    def __init__(self, body, id):
        """ The constructor method."""

        self.body = body
        self.id = id

        super().__init__(self.body, scale = 0.3, center_x = 1500, center_y = 1500)
        #calculate_hit_box = False

    def get_id(self):
        """ Returns the id of a pic object. """

        return self.id

class Name(arcade.Sprite):
    """ Class for the names. """

    def __init__(self, body, id):
        """ The constractor method."""

        self.body = body
        self.id = id
        super().__init__(self.body, scale = 0.3, center_x = 2000, center_y = 2000)

    def get_id(self):
        """ Returns the id of a name object. """

        return self.id


def main():
    """ The main function. """

    # Calls the Game class.
    window = Game()

    # Calls the setup method.
    window.setup()

    # Displays the window.
    arcade.run()



main()
