import tensorflow as tf

def load_pb_model(pb_file):
    with tf.io.gfile.GFile(pb_file, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.compat.v1.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="")

    return graph

pb_file = "E:/PythonProjectMain/AI/Models/20180402-114759.pb"
graph = load_pb_model(pb_file)

# Kiểm tra các tensor trong mô hình
for op in graph.get_operations():
    print(op.name)
