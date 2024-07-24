import 'dart:convert';
import 'dart:developer';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:multi_dropdown/multiselect_dropdown.dart';
import 'package:http/http.dart';
import 'package:http_parser/http_parser.dart';

enum PreprocessingMethods { augmentation, clahe, filtering, white_balancing }

class NerfForm extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return NerfState();
  }
}

class NerfState extends State<NerfForm> {
  Map values = {
    'preprocessing': <List>[],
    'estimator': 'colmap',
    'model': 'nerf'
  };
  showLoaderDialog(BuildContext context) {
    AlertDialog alert = AlertDialog(
      title: Text('Reconstructing'),
      content: ConstrainedBox(
          constraints: BoxConstraints.tight(Size(200, 200)),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(),
              Container(
                  margin: EdgeInsets.only(left: 7),
                  child: Text("Please Wait...")),
            ],
          )),
    );
    showDialog(
      barrierDismissible: false,
      context: context,
      builder: (BuildContext context) {
        return alert;
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      child: Column(mainAxisAlignment: MainAxisAlignment.start, children: [
        MultiSelectDropDown<int>(
          onOptionSelected: (List<ValueItem> selectedOptions) {
            values['preprocessing'] = selectedOptions.map((x) {
              return PreprocessingMethods.values[x.value].name;
            }).toList();
          },
          onOptionRemoved: (int index, ValueItem<int> option) {
            values['preprocessing']
                .remove(PreprocessingMethods.values[option.value!].name);
          },
          options: const <ValueItem<int>>[
            ValueItem(label: 'Augmentation', value: 0),
            ValueItem(label: 'CLAHE', value: 1),
            ValueItem(label: 'Filtering', value: 2),
            ValueItem(label: 'White Balancing', value: 3),
          ],
          selectionType: SelectionType.multi,
          chipConfig: const ChipConfig(wrapType: WrapType.wrap),
          dropdownHeight: 300,
          optionTextStyle: const TextStyle(fontSize: 16),
          selectedOptionIcon: const Icon(Icons.check_circle),
          hint: 'Preprocessing Pipeline',
        ),
        Divider(
          height: 20,
          color: Colors.transparent,
        ),
        DropdownButtonFormField(
            hint: Text('Pose Estimator'),
            borderRadius: BorderRadius.all(Radius.circular(20)),
            decoration: InputDecoration(
                contentPadding: EdgeInsets.fromLTRB(10, 0, 0, 0)),
            items: const [
              DropdownMenuItem(
                value: 'colmap',
                child: Text("Colmap"),
              ),
              DropdownMenuItem(value: 'hloc', child: Text("Hloc"))
            ],
            onChanged: (value) {
              values['estimator'] = value;
            }),
        Divider(
          height: 30,
          color: Colors.transparent,
        ),
        TextButton(
            onPressed: () async {
              try {
                FilePickerResult? file = await FilePicker.platform
                    .pickFiles(withReadStream: true, withData: false);
                if (file != null) {
                  showLoaderDialog(context);
                  String pipelineProps = json.encode(this.values);
                  var metadata = utf8.encode(pipelineProps);
                  StreamedRequest req = StreamedRequest(
                      'POST', Uri.parse("http://127.0.0.1:5000/start_nerf"));
                  req.headers.addAll({
                    'Content-Type': 'application/octet-stream',
                    'boundary': metadata.length.toString(),
                  });
                  req.contentLength = file.files.first.size + metadata.length;

                  req.sink.add(metadata);
                  req.sink.addStream(file.files.first.readStream!);
                  var res = await req.send();
                  //List<int> data = metadata + file.files.first.bytes!;
                  /*var res =
                      await post(Uri.parse("http://127.0.0.1:5000/start_nerf"),
                          headers: {
                            'Content-Type': 'application/octet-stream',
                            'boundary': metadata.length.toString(),
                          },
                          body: data,
                          encoding: Utf8Codec());*/
                }
              } catch (ex) {
                ex.toString();
              } finally {
                Navigator.of(context, rootNavigator: true).pop();
              }
            },
            child: const Text('Submit'))
      ]),
    );
  }
}
