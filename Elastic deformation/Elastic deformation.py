import Sofa.Gui

obj = "liver.msh"

def createScene(root_node):
    root_node.dt = 0.01                     # 步长dt
    root_node.gravity = [0, 0, 0]           # 场景重力g
    config = root_node.addChild("Config")   # 添加所需插件
    config.addObject('RequiredPlugin', name="Sofa.Component.IO.Mesh", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.LinearSolver.Iterative", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Mass", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.ODESolver.Backward", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.StateContainer", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.GL.Component.Rendering3D", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Topology.Container.Dynamic", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.SolidMechanics.FEM.Elastic", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Topology.Mapping", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Mapping.Linear", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Constraint.Projective", printLog=False)

    root_node.addObject("DefaultAnimationLoop") # 默认物理动画循环

    root_node.addObject("MeshGmshLoader", name="meshLoaderCoarse", filename=obj) # OBJ模型加载器

    liver = root_node.addChild("Liver")
    liver.addObject("EulerImplicitSolver") # 欧拉隐式求解器求解动力学方程
    liver.addObject("CGLinearSolver", iterations=100, tolerance=0.1, threshold=0.1) # 共轭梯度线性求解器
    liver.addObject("TetrahedronSetTopologyContainer", name="topo", src="@../meshLoaderCoarse") # 四面体拓扑容器
    liver.addObject("MechanicalObject", template="Vec3d", name="MechanicalModel", showObject=False) # 机械对象
    liver.addObject("TetrahedronFEMForceField", name="FEM", youngModulus=700, poissonRatio=0.45, method="large") # 四面体有限元应力场
    liver.addObject("FixedProjectiveConstraint", name="FixedProjectiveConstraint", indices=[1,300,500]) # 固定投影约束
    liver.addObject("MeshMatrixMass", massDensity=0.0005, topology="@topo") # 质量属性定义

    extract_surface = liver.addChild("ExtractSurface")
    surface_container = extract_surface.addObject("TriangleSetTopologyContainer", name="Container") # 三角形拓扑容器
    extract_surface.addObject("TriangleSetTopologyModifier", name="Modifier") # 三角形拓扑求解器
    extract_surface.addObject("Tetra2TriangleTopologicalMapping", input="@../topo", output="@Container") # 四面体网格生成三角形网格

    visual = extract_surface.addChild("Visual")
    visual_model = visual.addObject("OglModel", name="VisualModel", color=[1, 0, 0]) # OpenGL渲染模型
    visual.addObject("IdentityMapping", name="Mapping", input="@..", output="@VisualModel") # 身份映射

if __name__ == "__main__":
    # 创建场景
    root = Sofa.Core.Node("root")
    # 场景构建
    createScene(root)
    # 场景初始化
    Sofa.Simulation.initRoot(root)
    # 场景可视化
    Sofa.Gui.GUIManager.Init("scene","qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1080, 800)
    Sofa.Gui.GUIManager.MainLoop(root)
