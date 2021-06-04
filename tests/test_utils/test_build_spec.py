import os
from pathlib import Path
from bioimageio.spec import schema
from bioimageio.spec.utils import yaml


def test_build_spec_pickle(rf_config_path):
    from bioimageio.spec.utils.build_spec import build_spec

    source = yaml.load(rf_config_path)

    root = rf_config_path.parents[0]

    weight_path = os.path.join(root, source["weights"]["pickle"]["source"])
    assert os.path.exists(weight_path), weight_path
    test_inputs = [os.path.join(root, pp) for pp in source["test_inputs"]]
    test_outputs = [os.path.join(root, pp) for pp in source["test_outputs"]]

    cite = {"source": "https://citation.com"}
    attachments = {"files": "./some_local_file", "urls": ["https://attachment1.com", "https://attachment2.com"]}

    raw_model = build_spec(
        source=source["source"],
        model_kwargs=source["kwargs"],
        weight_uri=weight_path,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        name=source["name"],
        description=source["description"],
        authors=source["authors"],
        tags=source["tags"],
        license=source["license"],
        documentation=source["documentation"],
        covers=source["covers"],
        dependencies=source["dependencies"],
        cite=cite,
        attachments=attachments,
        input_name="raw",
        input_min_shape=[1, 1],
        input_step=[0, 0],
        output_reference="raw",
        output_scale=[1, 1],
        output_offset=[0, 0],
    )
    serialized = schema.Model().dump(raw_model)
    assert type(serialized) == type(source)


def test_build_spec_pytorch(UNet2DNucleiBroad_model_url):
    from bioimageio.spec.utils.build_spec import build_spec, _get_local_path

    config_path = _get_local_path(UNet2DNucleiBroad_model_url)
    assert os.path.exists(config_path), config_path
    source = yaml.load(Path(config_path))

    weight_source = source["weights"]["pytorch_state_dict"]["source"]
    test_inputs = [
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/unet2d_nuclei_broad/test_input.npy"
    ]
    test_outputs = [
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/unet2d_nuclei_broad/test_output.npy"
    ]

    cite = {entry["text"]: entry["doi"] if "doi" in entry else entry["url"] for entry in source["cite"]}

    raw_model = build_spec(
        source=source["source"],
        model_kwargs=source["kwargs"],
        weight_uri=weight_source,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        name=source["name"],
        description=source["description"],
        authors=source["authors"],
        tags=source["tags"],
        license=source["license"],
        documentation=source["documentation"],
        covers=source["covers"],
        dependencies=source["dependencies"],
        cite=cite,
    )
    serialized = schema.Model().dump(raw_model)
    assert type(serialized) == type(source)


def test_build_spec_onnx(UNet2DNucleiBroad_model_url):
    from bioimageio.spec.utils.build_spec import build_spec, _get_local_path

    config_path = _get_local_path(UNet2DNucleiBroad_model_url)
    assert os.path.exists(config_path), config_path
    source = yaml.load(Path(config_path))

    weight_source = (
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/"
        + "unet2d_nuclei_broad/weights.onnx"
    )
    test_inputs = [
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/unet2d_nuclei_broad/test_input.npy"
    ]
    test_outputs = [
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/unet2d_nuclei_broad/test_output.npy"
    ]

    cite = {entry["text"]: entry["doi"] if "doi" in entry else entry["url"] for entry in source["cite"]}

    raw_model = build_spec(
        weight_uri=weight_source,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        name=source["name"],
        description=source["description"],
        authors=source["authors"],
        tags=source["tags"],
        license=source["license"],
        documentation=source["documentation"],
        covers=source["covers"],
        dependencies=source["dependencies"],
        cite=cite,
    )
    serialized = schema.Model().dump(raw_model)
    assert type(serialized) == type(source)


def test_build_spec_torchscript(UNet2DNucleiBroad_model_url):
    from bioimageio.spec.utils.build_spec import build_spec, _get_local_path

    config_path = _get_local_path(UNet2DNucleiBroad_model_url)
    assert os.path.exists(config_path), config_path
    source = yaml.load(Path(config_path))

    weight_source = (
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/" + "unet2d_nuclei_broad/weights.pt"
    )
    test_inputs = [
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/unet2d_nuclei_broad/test_input.npy"
    ]
    test_outputs = [
        "https://github.com/bioimage-io/pytorch-bioimage-io/raw/master/specs/models/unet2d_nuclei_broad/test_output.npy"
    ]

    cite = {entry["text"]: entry["doi"] if "doi" in entry else entry["url"] for entry in source["cite"]}

    raw_model = build_spec(
        weight_uri=weight_source,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        name=source["name"],
        description=source["description"],
        authors=source["authors"],
        tags=source["tags"],
        license=source["license"],
        documentation=source["documentation"],
        covers=source["covers"],
        dependencies=source["dependencies"],
        cite=cite,
        weight_type="pytorch_script",
    )
    serialized = schema.Model().dump(raw_model)
    assert type(serialized) == type(source)


def test_build_spec_keras(FruNet_model_url):
    from bioimageio.spec.utils.build_spec import build_spec, _get_local_path

    config_path = _get_local_path(FruNet_model_url)
    assert os.path.exists(config_path), config_path
    source = yaml.load(Path(config_path))

    weight_source = "https://zenodo.org/record/4156050/files/fully_residual_dropout_segmentation.h5"
    test_inputs = ["https://github.com/deepimagej/models/raw/master/fru-net_sev_segmentation/exampleImage.npy"]
    test_outputs = ["https://github.com/deepimagej/models/raw/master/fru-net_sev_segmentation/resultImage.npy"]
    cite = {entry["text"]: entry["doi"] if "doi" in entry else entry["url"] for entry in source["cite"]}

    raw_model = build_spec(
        weight_uri=weight_source,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        name=source["name"],
        description=source["description"],
        authors=source["authors"],
        tags=source["tags"],
        license=source["license"],
        documentation=source["documentation"],
        covers=source["covers"],
        cite=cite,
        tensorflow_version="1.12",
    )

    serialized = schema.Model().dump(raw_model)
    assert type(serialized) == type(source)


def test_build_spec_tf(FruNet_model_url):
    from bioimageio.spec.utils.build_spec import build_spec, _get_local_path

    config_path = _get_local_path(FruNet_model_url)
    assert os.path.exists(config_path), config_path
    source = yaml.load(Path(config_path))

    weight_source = "https://zenodo.org/record/4156050/files/tensorflow_saved_model_bundle.zip"
    test_inputs = ["https://github.com/deepimagej/models/raw/master/fru-net_sev_segmentation/exampleImage.npy"]
    test_outputs = ["https://github.com/deepimagej/models/raw/master/fru-net_sev_segmentation/resultImage.npy"]
    cite = {entry["text"]: entry["doi"] if "doi" in entry else entry["url"] for entry in source["cite"]}

    raw_model = build_spec(
        weight_uri=weight_source,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        name=source["name"],
        description=source["description"],
        authors=source["authors"],
        tags=source["tags"],
        license=source["license"],
        documentation=source["documentation"],
        covers=source["covers"],
        cite=cite,
        tensorflow_version="1.12",
    )

    serialized = schema.Model().dump(raw_model)
    assert type(serialized) == type(source)


def test_build_spec_tfjs(FruNet_model_url):
    from bioimageio.spec.utils.build_spec import build_spec, _get_local_path

    config_path = _get_local_path(FruNet_model_url)
    assert os.path.exists(config_path), config_path
    source = yaml.load(Path(config_path))

    weight_source = (
        "https://raw.githubusercontent.com/deepimagej/tensorflow-js-models/main/"
        "fru-net_sev_segmentation_tf_js_model/model.json"
    )
    test_inputs = ["https://github.com/deepimagej/models/raw/master/fru-net_sev_segmentation/exampleImage.npy"]
    test_outputs = ["https://github.com/deepimagej/models/raw/master/fru-net_sev_segmentation/resultImage.npy"]
    cite = {entry["text"]: entry["doi"] if "doi" in entry else entry["url"] for entry in source["cite"]}

    raw_model = build_spec(
        weight_uri=weight_source,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        name=source["name"],
        description=source["description"],
        authors=source["authors"],
        tags=source["tags"],
        license=source["license"],
        documentation=source["documentation"],
        covers=source["covers"],
        cite=cite,
    )

    serialized = schema.Model().dump(raw_model)
    assert type(serialized) == type(source)
