import pychrono as chrono
import pychrono.irrlicht as chronoirr


class ChronoVisualizer:
    def __init__(
        self, system: chrono.ChSystem, properties: dict = None
    ) -> None:
        self.__visualizer = chronoirr.ChVisualSystemIrrlicht()
        self.__system = system
        self.__properties = properties if properties is not None else {}

    def setup(self):
        self.__visualizer.AttachSystem(self.__system)
        self.__visualizer.SetWindowSize(1024, 768)
        self.__visualizer.SetWindowTitle("3D muscle-based walking sim")
        self.__visualizer.Initialize()
        skybox_texture = self.__properties.get("textures", {}).get(
            "skybox", None
        )
        if skybox_texture:
            self.__visualizer.AddSkyBox(skybox_texture)
        else:
            self.__visualizer.AddSkyBox()
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

    def close(self):
        self.__visualizer.GetDevice().closeDevice()
