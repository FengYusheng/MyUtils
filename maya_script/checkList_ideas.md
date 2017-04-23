### Merge all vertices

####  precode
    vertices = pm.ls(selection=True)
    print vertices[0]
    # make pCubeShape3.vtx[0:7] iteratble

    vtx_iter = vertices[0].indicesIter()
    for vtx in vtx_iter:
        print vtx

    a = pm.dt.point(0.0, 0.0, 0.0)
    b = pm.dt.point(0.0, 0.0, 0.0)
    a == b # True    


#### Idea
  check whether two vertices which have same position exists.
