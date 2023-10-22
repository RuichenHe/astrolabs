from PySide2.QtWidgets import QWidget, QSizePolicy
from PySide2.QtGui import QColor, QPainter, QPixmap, QPen, QImage
from PySide2.QtCore import Qt, Signal, Slot

import os

class Star():
    def __init__(self, star_id, x, y, mag, color, selected=False):
        self._id = star_id
        self._x = x
        self._y = y
        self._mag = mag
        self._color = color
        self._selected = selected

class StarData():
    def __init__(self):
        self._stars = []

    def add_star(self, star):
        self._stars.append(star)

    def get_star(self, ix):
        return self._stars[ix]

    def size(self):
        return len(self._stars)
    
class StarImage(QWidget):
    star_selected = Signal(bool, int)
    def __init__(self, parent=None):
        super(StarImage, self).__init__(parent)
        
        self.star_data_ = None
        self.c_scale = 0.8
        self.star_size = 48.0
        self.cross_size = 12
        self.rect_size = 16
        self.star_pen_width = 2
        self.cursor_pen_width = 3
        self.single_selection_mode = False
        self.selected = False
        self.currentSelectId = -1
        self.image_h = None
        self.image_w = None
        self.setMouseTracking(True)
        self.setCursor(Qt.BlankCursor)

        # Load the background image
        try:
            self.background_ = QPixmap(os.path.join(os.getcwd(), '..','assets', 'background', 'm15gc.png'))
            aspect_ratio = self.background_.width() / float(self.background_.height())
        except:
            self.background_ = QPixmap(os.path.join(os.getcwd(),'assets', 'background', 'm15gc.png'))
            aspect_ratio = self.background_.width() / float(self.background_.height())

        aspect_ratio = self.background_.width() / float(self.background_.height())
        self.setMinimumHeight(self.background_.height() / 2)
        self.setMinimumWidth(aspect_ratio * (self.background_.height() / 2))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Initialize visual settings
        # These might require adjustments based on the original C++ settings
        self.star_indicator_pen_ = QPen(QColor(0, 114, 178, 180), self.star_pen_width)
        self.star_indicator_pen_on_ = QPen(QColor(100, 174, 248, 180), self.star_pen_width)
        self.star_measured_pen_ = QPen(QColor(213, 94, 0, 255), self.cursor_pen_width)
        self.cursor_pen_ = QPen(Qt.white)
        self.secondary_cursor_pen_ = QPen(Qt.white, 3)

        # Other initialization here as needed
        # ... 
        self.update()


    def set_color_channel(self, channel):
        if channel == 0:
            return

        image = self.background_.toImage()

        for i in range(self.background_.width()):
            for j in range(self.background_.height()):
                color = QColor(image.pixel(i, j))

                if channel == 1:
                    image.setPixel(i, j, QColor(color.red(), 0, 0).rgb())
                elif channel == 2:
                    image.setPixel(i, j, QColor(0, color.green(), 0).rgb())
                elif channel == 3:
                    image.setPixel(i, j, QColor(0, 0, color.blue()).rgb())
                elif channel == 4:
                    image.setPixel(i, j, QColor(color.red(), color.green(), 0).rgb())
                elif channel == 5:
                    image.setPixel(i, j, QColor(color.blue(), color.blue(), color.blue()).rgb())
                elif channel == 6:
                    image.setPixel(i, j, QColor(color.red(), color.red(), color.red()).rgb())
                elif channel == 50:
                    image.setPixel(i, j, QColor(self.c_scale * color.blue(), self.c_scale * color.blue(), color.blue()).rgb())
                elif channel == 60:
                    image.setPixel(i, j, QColor(color.red(), self.c_scale * color.red(), self.c_scale * color.red()).rgb())
                elif channel == 7:
                    image.setPixel(i, j, QColor(0, 0, 0).rgb())  # Equivalent to color.black()

        self.background_ = QPixmap.fromImage(image)

    def draw_cursor(self, painter, x_pos, y_pos, selected):
        #self.image_w  = self.width()
        #self.image_h  = self.height()
        if selected:
            painter.setPen(self.secondary_cursor_pen_)
            painter.drawEllipse(x_pos * self.image_w - self.star_size / 2, y_pos * self.image_h - self.star_size / 2, self.star_size, self.star_size)
        else:
            painter.setPen(self.cursor_pen_)
            painter.drawRect(x_pos * self.image_w - self.rect_size / 2, y_pos * self.image_h - self.rect_size / 2, self.rect_size, self.rect_size)
        

        painter.drawLine(0, y_pos * self.image_h, x_pos * self.image_w - self.rect_size / 2, y_pos * self.image_h)
        
        painter.drawLine(x_pos * self.image_w + self.rect_size / 2, y_pos * self.image_h, self.image_w, y_pos * self.image_h)
        
        painter.drawLine(x_pos * self.image_w, 0, x_pos * self.image_w, y_pos * self.image_h - self.rect_size / 2)
        
        painter.drawLine(x_pos * self.image_w, y_pos * self.image_h + self.rect_size / 2, x_pos * self.image_w, self.image_h)
    

    def hit_test(self):
        # We want to select the closest point
        min_distance = (0.5 * self.star_size) ** 2
        selected = -1
        image_w_ = self.image_w
        image_h_ = self.image_h
        # First check for non-selected items
        
        for i in range(0,self.star_data_.size()):
            s = self.star_data_.get_star(i)
            dx = int(s._x * image_w_ - self.mouse_x_)
            dy = int(s._y * image_h_ - self.mouse_y_)
            dr = dx**2 + dy**2

            if min_distance > dr:
                selected = i
                min_distance = dr
        return selected
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        aspect_ratio = self.background_.width() / float(self.background_.height())

        image_w_ = self.width()
        image_h_ = self.height()

        if image_w_ > image_h_:
            image_w_ = aspect_ratio * self.height()
        else:
            image_h_ = self.width() / aspect_ratio

        # HACK:
        if image_w_ > self.width():
            image_w_ = self.width()
            image_h_ = self.width() / aspect_ratio

        painter.drawPixmap(0, 0, image_w_, image_h_, self.background_)
        self.image_h = image_h_
        self.image_w = image_w_
        # Assuming star_data_ is a Python list or similar
        if not self.star_data_:
            return
        
        if self.single_selection_mode:
            if self.selected and self.currentSelectId > -1 and self.currentSelectId < self.star_data_.size():
                s = self.star_data_.get_star(self.currentSelectId)  # Assuming this is a list of Star objects
                self.draw_cursor(painter, s._x, s._y, True)
            return
        #Draw the all stars that haven't been measured yet
        #print("Star size", self.star_data_.size())
        for i in range(0,self.star_data_.size()):
            painter.setPen(self.star_indicator_pen_)
            s = self.star_data_.get_star(i)

        #if (s->_selected) {
         #   continue;
        #}
            x = int(s._x * image_w_ - 0.5 * self.star_size)
            y = int(s._y * image_h_ - 0.5 * self.star_size)
            try:
                if ((s._x * image_w_ - self.mouse_x_)**2 + (s._y * image_h_ - self.mouse_y_)**2 < (0.5*self.star_size)**2):
                    painter.setPen(self.star_indicator_pen_on_)
            except:
                print("Cursor not ready")
            if self.currentSelectId == i:
                painter.setPen(self.star_measured_pen_)
                painter.drawEllipse(x, y, self.star_size, self.star_size)
                painter.drawLine(s._x * image_w_ - self.cross_size, s._y * image_h_ - self.cross_size, s._x * image_w_ + self.cross_size, s._y * image_h_ + self.cross_size)

                painter.drawLine(s._x * image_w_ + self.cross_size, s._y * image_h_ - self.cross_size, s._x * image_w_ - self.cross_size, s._y * image_h_ + self.cross_size)
            elif s._selected == False:
                painter.drawEllipse(x, y, self.star_size, self.star_size)

        painter.setPen(self.star_measured_pen_)
        try:
            self.draw_cursor(painter, float(self.mouse_x_) / image_w_, float(self.mouse_y_) / image_h_, False)
        except:
            pass
        painter.end()



    def mouseMoveEvent(self, event):
        self.mouse_x_ = event.x()
        self.mouse_y_ = event.y()
        self.update()

    def mouseReleaseEvent(self, event):
        self.currentSelectId = self.hit_test()
        self.update()
        self.star_selected.emit(self.currentSelectId != -1, self.currentSelectId)
        

    def set_star_data(self, star_data):
        self.star_data_ = star_data

    def set_single_mode(self, mode):
        self.single_selection_mode = mode
        print(self.single_selection_mode)
    # Implement other methods like mouseReleaseEvent, setColorChannel, etc.
    # ...

    @Slot(bool, int)
    def on_selection_changed(self, selected, star_id):
        if not self.single_selection_mode:
            return

        self.selected = selected
        self.currentSelectId = star_id
        self.update()