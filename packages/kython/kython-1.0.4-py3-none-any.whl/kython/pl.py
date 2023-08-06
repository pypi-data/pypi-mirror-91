import matplotlib.pyplot as plt
from matplotlib.patches import *
import pp

def SequenceHomogeneity(pValueList:list,posList:list,pValueAccepted:float) -> None:
        


        #Starting points for shapes
        startingX=0
        startingY=0.25
        
        #Shapes configuration 
        blueRectangleHeight=1
        blueRectangleLength=100
        blueRectangleColor='blue'
        
        redRectanglesHeight=0.3
        redRectanglesColor='red'
        
        ticksColor="white"
        ticksHeight=1
        
        #Creating shapes
        
        #Big Rectangle
        blueRectangle=Rectangle((startingX,startingY), width=blueRectangleLength,height=blueRectangleHeight,color=blueRectangleColor)
        #Tiny Rectangles
        
        #Ticks
        listTicks=[]
        lengthGenome=posList[-1]
        for position in posList:
                positionScaled=(position/lengthGenome)*100
                line=plt.Line2D((positionScaled,positionScaled),(startingY,startingY+ticksHeight),linewidth=0.5,color=ticksColor)
                listTicks.append(line)
        
        
        
        
        
        
        
        #Creating the figure
        fig=plt.figure()#figsize=(blueRectangleLength*2,blueRectangleHeight*2))
        ax=fig.add_subplot(111)
        

        #Adding shapes to the ax
        ax.add_patch(blueRectangle)
        
        for tick in listTicks:
                ax.add_line(tick)
        
        #Adjusting ax
        ax.axis("scaled")
        
        
        return fig




if __name__=='__main__':


        #fig, ax=plt.subplots()
        listpVal,listPos=pp.SequenceHomogeneity('./testGenome.fna',3,10000)
        fig=SequenceHomogeneity(listpVal,listPos,0.05)
        plt.show()
