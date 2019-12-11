import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

matplotlib.rcParams['toolbar'] = 'None'
img = plt.imread("map.jpg")

fig, ax1 = plt.subplots()
plt.subplots_adjust(left=0,bottom=0,right=1,top=1)
figManager = plt.get_current_fig_manager()
figManager.full_screen_toggle()
 
def animate(i):
    origin_x=910
    origin_y=625
    my_lat="39.739235"
    my_long="-104.990250"
    graph_data = open('IP_logins.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            ip, lat, long = line.split(',')
            xs.append(origin_x+((14*float(long))/3))
            ys.append(origin_y-(5.2*float(lat)))
            xs.append(origin_x+((14*float(my_long))/3))
            ys.append(origin_y-(5.2*float(my_lat)))
            
    ax1.clear()
    ax1.imshow(img)
    ax1.plot(xs, ys)
    ax1.plot(origin_x+((14*float(my_long))/3),origin_y-(5.2*float(my_lat)),'g*')
    
    
ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)
plt.show()

