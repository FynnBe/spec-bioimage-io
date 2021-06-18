# BioImage.IO Resource Description File Specification 0.3.2
This specification defines the fields used in a general BioImage.IO-complaint resource description file (`RDF`).
An RDF is stored as a YAML file. 

The RDF contains mandatory and optional fields. In the following description, optional fields are indicated by _optional_.
_optional*_ with an asterisk indicates the field is optional depending on the value in another field.

* `format_version` _String_ Version of the BioImage.IO Model Resource Description File Specification used.
This is mandatory, and important for the consumer software to verify before parsing the fields.
The recommended behavior for the implementation is to keep backward compatibility and throw an error if the model yaml
is in an unsupported format version. The current format version described here is
0.3.2
* `cite` _List\[CiteEntry\]_ A citation entry or list of citation entries.
Each entry contains a mandatory `text` field and either one or both of `doi` and `url`.
E.g. the citation for the model architecture and/or the training data used. is a Dict with the following keys:
  * `text` _String_ 
  * `doi` _optional* String_ 
  * `url` _optional* String_ 
* `description` _String_ A string containing a brief description.
* `documentation` _RelativeLocalPath→Path_ Relative path to file with additional documentation in markdown. This means: 1) only relative file path is allowed 2) the file must be in markdown format with `.md` file name extension 3) URL is not allowed. It is recommended to use `README.md` as the documentation name.
* `name` _String_ name of the resource, a human-friendly name
* `tags` _List\[String\]_ A list of tags.
* `type` _String_ 
* `attachments` _optional* Dict\[String, Union\[URI→String | List\[URI→String\]\]\]_ Dictionary of text keys and URI (or a list of URI) values to additional, relevant files. E.g. we can place a list of URIs under the `files` to list images and other files that this resource depends on.
* `authors` _optional List\[Author\]_ A list of authors. The authors are the creators of the specifications and the primary points of contact.
* `badges` _optional List\[Badge\]_ a list of badges
* `config` _optional Dict\[Any, Any\]_ A custom configuration field that can contain any keys. It can be very specific to a framework or specific tool. To avoid conflicted definitions, it is recommended to wrap configuration into a sub-field named with the specific framework or tool name.
* `covers` _optional List\[URI→String\]_ A list of cover images provided by either a relative path to the model folder, or a hyperlink starting with 'https'.Please use an image smaller than 500KB and an aspect ratio width to height of 2:1. The supported image formats are: 'jpg', 'png', 'gif'.
* `download_url` _optional String_ recommended url to the zipped file if applicable
* `git_repo` _optional String_ A url to the git repository, e.g. to Github or Gitlab.
* `icon` _optional String_ an icon for the resource
* `license` _optional String_ A [SPDX license identifier](https://spdx.org/licenses/)(e.g. `CC-BY-4.0`, `MIT`, `BSD-2-Clause`). We don't support custom license beyond the SPDX license list, if you need that please send an Github issue to discuss your intentions with the community.
* `source` _optional URI→String_ url to the source of the resource
* `version` _optional StrictVersion→String_ The version number of the model. The version number format must be a string in `MAJOR.MINOR.PATCH` format following the guidelines in Semantic Versioning 2.0.0 (see https://semver.org/), e.g. the initial version number should be `0.1.0`.
