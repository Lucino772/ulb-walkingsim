import pychrono as chrono
import pychrono.irrlicht as chronoirr


class ChronoVisualizer:
    def __init__(self, system: chrono.ChSystem) -> None:
        self.__visualizer = chronoirr.ChVisualSystemIrrlicht()
        self.__system = system

    def setup(self):
        self.__visualizer.AttachSystem(self.__system)
        self.__visualizer.SetWindowSize(1024, 768)
        self.__visualizer.SetWindowTitle("3D muscle-based walking sim")
        self.__visualizer.Initialize()
        self.__visualizer.AddSkyBox("resources/materials/skybox/pink_sky/")
        self.__visualizer.AddCamera(chrono.ChVectorD(11, 3, 12))
        self.__visualizer.AddTypicalLights()
        #  self.__visualizer.SetShadows(True)

    def render(self):
        self.__visualizer.BeginScene()
        self.__visualizer.Render()
        #  self.__visualizer.ShowInfoPanel(True)
        self.__visualizer.EndScene()

    def refresh(self):
        self.__visualizer.BindAll()

    def check(self):
        return self.__visualizer.Run()
