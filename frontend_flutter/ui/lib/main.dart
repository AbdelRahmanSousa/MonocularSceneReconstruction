import 'package:flutter/material.dart';
import 'package:ui/form.dart';
import 'package:ui/theme.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Monocular 3D Scene Reconstruction',
      theme: ThemeData(colorScheme: MaterialTheme.lightScheme()),
      home: Scaffold(
        body: Row(children: [
          Expanded(
              flex: 1,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Expanded(
                      flex: 1,
                      child: Padding(
                          padding: EdgeInsets.only(top: 40),
                          child: Text(
                            'Choose Methods',
                            style: Theme.of(context).textTheme.headlineLarge,
                          ))),
                  Expanded(
                      flex: 2,
                      child: ConstrainedBox(
                          constraints:
                              const BoxConstraints(minWidth: 50, maxWidth: 350),
                          child: NerfForm()))
                ],
              )),
          Expanded(
              flex: 2,
              child: Container(
                decoration: const BoxDecoration(
                    image: DecorationImage(
                        repeat: ImageRepeat.noRepeat,
                        fit: BoxFit.fill,
                        image: AssetImage('assets/wallpaper.png'))),
              ))
        ]),
      ),
    );
  }
}
