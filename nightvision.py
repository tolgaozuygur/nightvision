from picamera import mmal, mmalobj as mo
from signal import pause
from time import sleep
import sys, pygame, time, os
from gpiozero import Button

#init stuff
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
CAM_FPS_LIST = [10,30,60,90]
CAM_WIDTH = 261 #300
CAM_HEIGHT = 348 #400
CAM_ROTATION = 90
CAM_HORIZONTAL_OFFSET = 18
POWER_DOWN_BUTTON_DUR = 5 #seconds

cam_fps_id = 1

#draw black background and fps with pygame
def updateFpsText():
        fps_text = font.render(str(CAM_FPS_LIST[cam_fps_id]) + "fps", True, green, black)
        fps_text_rect = fps_text.get_rect()
        fps_text_rect.center = (CAM_HORIZONTAL_OFFSET-(CAM_WIDTH/2),((SCREEN_HEIGHT+CAM_HEIGHT)/2)+7)
        screen.blit(fps_text, fps_text_rect)
        fps_text_rect.center = (SCREEN_WIDTH-(CAM_HORIZONTAL_OFFSET+(CAM_WIDTH/2)), ((SCREEN_HEIGHT+CAM_HEIGHT)/2)+7)
        screen.blit(fps_text, fps_text_rect)
        pygame.display.flip()

green = (0, 255, 0)
black = (0, 0, 0)
pygame.init()
font = pygame.font.Font(None, 24)
size = width, height = 800, 480
screen = pygame.display.set_mode(size)
screen.fill(black)
pygame.display.toggle_fullscreen()
pygame.mouse.set_visible(False)
pygame.display.update()
updateFpsText()

#use mmal to draw camera preview for each eye
camera = mo.MMALCamera()
splitter = mo.MMALSplitter()
render_l = mo.MMALRenderer()
render_r = mo.MMALRenderer()

camera.outputs[0].framesize = (CAM_WIDTH, CAM_HEIGHT)
camera.outputs[0].framerate = CAM_FPS_LIST[cam_fps_id]
camera.outputs[0].params[mmal.MMAL_PARAMETER_ROTATION] = CAM_ROTATION
camera.outputs[0].commit()

p = render_l.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]
p.set = mmal.MMAL_DISPLAY_SET_FULLSCREEN | mmal.MMAL_DISPLAY_SET_DEST_RECT
p.fullscreen = False
p.dest_rect = mmal.MMAL_RECT_T(CAM_HORIZONTAL_OFFSET, (SCREEN_HEIGHT-CAM_HEIGHT)/2, CAM_WIDTH, CAM_HEIGHT)
render_l.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION] = p
p.dest_rect = mmal.MMAL_RECT_T(SCREEN_WIDTH-(CAM_WIDTH+CAM_HORIZONTAL_OFFSET), (SCREEN_HEIGHT-CAM_HEIGHT)/2, CAM_WIDTH, CAM_HEIGHT)
render_r.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION] = p

splitter.connect(camera.outputs[0])
splitter.connection.enable()
render_l.connect(splitter.outputs[0])
render_l.connection.enable()
render_r.connect(splitter.outputs[1])
render_r.connection.enable()

#main loop
funcButton = Button(26)
funcButtonDownStartTime = 0
while True:
        if funcButton.is_pressed:
                if funcButtonDownStartTime == 0:
                        funcButtonDownStartTime = time.time()
                else:
                        if (time.time() - funcButtonDownStartTime) >= POWER_DOWN_BUTTON_DUR:
                                os.system("sudo shutdown now -h")
        else:
                if funcButtonDownStartTime != 0:
                        #disable connections
                        splitter.connection.disable()
                        render_l.connection.disable()
                        render_r.connection.disable()
                        #change fps
                        cam_fps_id += 1
                        if cam_fps_id >= len(CAM_FPS_LIST):
                                cam_fps_id = 0
                        print(CAM_FPS_LIST[cam_fps_id])
                        updateFpsText()
                        camera.outputs[0].framerate = CAM_FPS_LIST[cam_fps_id]
                        camera.outputs[0].commit()
                        #enable connections
                        splitter.connection.enable()
                        render_l.connection.enable()
                        render_r.connection.enable()
                        ###
                        print("Func button pressed")
                        funcButtonDownStartTime = 0
        time.sleep(0.1)



