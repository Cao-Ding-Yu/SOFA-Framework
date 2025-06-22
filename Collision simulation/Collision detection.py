import Sofa.Gui

obj1="ball.obj"
obj2="floor.obj"

# 场景构建
def createScene(rootNode):
    rootNode.dt=0.01                        # 配置调试步长
    rootNode.gravity=[0.0,-9.8,0.0]         # 配置重力
    config = rootNode.addChild("Config")    # 添加所需插件
    config.addObject('RequiredPlugin', name="Sofa.Component.AnimationLoop", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Collision.Detection.Algorithm", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Collision.Detection.Intersection", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Collision.Geometry", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Collision.Response.Contact", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Constraint.Lagrangian.Correction", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Constraint.Lagrangian.Solver", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.IO.Mesh", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.LinearSolver.Iterative", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Mapping.NonLinear", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Mass", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.ODESolver.Backward", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.StateContainer", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Topology.Container.Constant", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.Component.Visual", printLog=False)
    config.addObject('RequiredPlugin', name="Sofa.GL.Component.Rendering3D", printLog=False)

    # 碰撞系统配置
    rootNode.addObject('FreeMotionAnimationLoop') # 自由物理动画循环
    rootNode.addObject('CollisionPipeline') # 碰撞检测管道
    rootNode.addObject('BruteForceBroadPhase') # 暴力宽阶段碰撞检测
    rootNode.addObject('BVHNarrowPhase') # 层次包围盒窄阶段碰撞检测
    rootNode.addObject('GenericConstraintSolver', tolerance="1e-6", maxIterations="1000") # 通用约束求解器
    rootNode.addObject('RuleBasedContactManager', responseParams="mu="+str(0.0), response='FrictionContactConstraint')# 接触响应规则
    rootNode.addObject('LocalMinDistance', alarmDistance=10, contactDistance=5, angleCone=0.01) # 碰撞距离阈值

    # 创建球体
    sphere = rootNode.addChild("sphere")
    sphere.addObject('EulerImplicitSolver') # 欧拉隐式求解器求解动力学方程
    sphere.addObject('CGLinearSolver', iterations=25, tolerance=1e-05, threshold=1e-05) # 共轭梯度线性求解器
    sphere.addObject('MechanicalObject', template="Rigid3", translation2=[0., 0., 0.], rotation2=[0., 0., 0.]) # 机械对象
    sphere.addObject('UniformMass', vertexMass=[1.0, 1.0, [1., 0., 0., 0., 1., 0., 0., 0., 1.]]) # 质量属性定义
    sphere.addObject('UncoupledConstraintCorrection') # 约束校正

    # 添加球体碰撞模型
    collision = sphere.addChild('collision')
    collision.addObject('MeshOBJLoader', name="loader", filename=obj1, scale=45.0) # OBJ模型加载器
    collision.addObject('MeshTopology', src="@loader") # 拓扑容器
    collision.addObject('MechanicalObject') # 机械对象
    collision.addObject('PointCollisionModel') # 点碰撞模型
    collision.addObject('RigidMapping') # 刚体映射

    # 添加球体视图模型
    sphereVisu = sphere.addChild("VisualModel")
    sphereVisu.loader = sphereVisu.addObject('MeshOBJLoader', name="loader", filename=obj1) # OBJ模型加载器
    sphereVisu.addObject('OglModel', src="@loader", scale3d=[50]*3, color=[0., 1., 0.], updateNormals=False) # OpenGL渲染模型
    sphereVisu.addObject('RigidMapping') # 刚体映射

    # 创建地板
    floor = rootNode.addChild("floor")
    floor.addObject('MechanicalObject', name="mstate", template="Rigid3", translation2=[0.0,-300.0,0.0], rotation2=[0., 0., 0.]) # 机械对象

    # 添加地板碰撞模型
    floorCollis = floor.addChild('collision')
    floorCollis.addObject('MeshOBJLoader', name="loader", filename=obj2, scale=5.0) # OBJ模型加载器
    floorCollis.addObject('MeshTopology', src="@loader") # 拓扑容器
    floorCollis.addObject('MechanicalObject') # 机械对象
    floorCollis.addObject('TriangleCollisionModel', moving=False, simulated=False) # 三角形碰撞模型
    floorCollis.addObject('RigidMapping') # 刚体映射

    # 添加地板视图模型
    floorVisu = floor.addChild("VisualModel")
    floorVisu.loader = floorVisu.addObject('MeshOBJLoader', name="loader", filename=obj2) # OBJ模型加载器
    floorVisu.addObject('OglModel', src="@loader", scale3d=[5.0]*3, color=[1., 1., 0.], updateNormals=False) # OpenGL渲染模型
    floorVisu.addObject('RigidMapping') # 刚体映射


if __name__ == '__main__':
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
