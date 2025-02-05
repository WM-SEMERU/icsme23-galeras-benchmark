def test__sub__() -> None:
    data_a = np.array([1,-1,-2], dtype=np.int32)
    data_b = np.array([1,1,3], dtype=np.int32)
    data_c = np.array([0,-2,-5], dtype=np.int32)

    tensor_a = PassthroughTensor(child=data_a)
    tensor_b = PassthroughTensor(child=data_b)
    tensor_c = PassthroughTensor(child=data_c)

    assert tensor_a.__sub__(tensor_b) == tensor_c 