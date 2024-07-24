import "package:flutter/material.dart";

class MaterialTheme {
  final TextTheme textTheme;

  const MaterialTheme(this.textTheme);

  static ColorScheme lightScheme() {
    return const ColorScheme(
      brightness: Brightness.light,
      primary: Color(4278282109),
      surfaceTint: Color(4278282109),
      onPrimary: Color(4294967295),
      primaryContainer: Color(4289981439),
      onPrimaryContainer: Color(4278198055),
      secondary: Color(4283130474),
      onSecondary: Color(4294967295),
      secondaryContainer: Color(4291749616),
      onSecondaryContainer: Color(4278591013),
      tertiary: Color(4284046462),
      onTertiary: Color(4294967295),
      tertiaryContainer: Color(4292862207),
      onTertiaryContainer: Color(4279572791),
      error: Color(4290386458),
      onError: Color(4294967295),
      errorContainer: Color(4294957782),
      onErrorContainer: Color(4282449922),
      surface: Color(4294310653),
      onSurface: Color(4279704606),
      onSurfaceVariant: Color(4282402891),
      outline: Color(4285560956),
      outlineVariant: Color(4290758860),
      shadow: Color(4278190080),
      scrim: Color(4278190080),
      inverseSurface: Color(4281086259),
      inversePrimary: Color(4287025642),
      primaryFixed: Color(4289981439),
      onPrimaryFixed: Color(4278198055),
      primaryFixedDim: Color(4287025642),
      onPrimaryFixedVariant: Color(4278210143),
      secondaryFixed: Color(4291749616),
      onSecondaryFixed: Color(4278591013),
      secondaryFixedDim: Color(4289972948),
      onSecondaryFixedVariant: Color(4281616978),
      tertiaryFixed: Color(4292862207),
      onTertiaryFixed: Color(4279572791),
      tertiaryFixedDim: Color(4290888939),
      onTertiaryFixedVariant: Color(4282467429),
      surfaceDim: Color(4292271069),
      surfaceBright: Color(4294310653),
      surfaceContainerLowest: Color(4294967295),
      surfaceContainerLow: Color(4293915895),
      surfaceContainer: Color(4293586929),
      surfaceContainerHigh: Color(4293192171),
      surfaceContainerHighest: Color(4292797414),
    );
  }

  ThemeData light() {
    return theme(lightScheme());
  }

  static ColorScheme lightMediumContrastScheme() {
    return const ColorScheme(
      brightness: Brightness.light,
      primary: Color(4278208858),
      surfaceTint: Color(4278282109),
      onPrimary: Color(4294967295),
      primaryContainer: Color(4281106068),
      onPrimaryContainer: Color(4294967295),
      secondary: Color(4281353806),
      onSecondary: Color(4294967295),
      secondaryContainer: Color(4284577920),
      onSecondaryContainer: Color(4294967295),
      tertiary: Color(4282204257),
      onTertiary: Color(4294967295),
      tertiaryContainer: Color(4285493909),
      onTertiaryContainer: Color(4294967295),
      error: Color(4287365129),
      onError: Color(4294967295),
      errorContainer: Color(4292490286),
      onErrorContainer: Color(4294967295),
      surface: Color(4294310653),
      onSurface: Color(4279704606),
      onSurfaceVariant: Color(4282139719),
      outline: Color(4283981924),
      outlineVariant: Color(4285758592),
      shadow: Color(4278190080),
      scrim: Color(4278190080),
      inverseSurface: Color(4281086259),
      inversePrimary: Color(4287025642),
      primaryFixed: Color(4281106068),
      onPrimaryFixed: Color(4294967295),
      primaryFixedDim: Color(4278216058),
      onPrimaryFixedVariant: Color(4294967295),
      secondaryFixed: Color(4284577920),
      onSecondaryFixed: Color(4294967295),
      secondaryFixedDim: Color(4282998631),
      onSecondaryFixedVariant: Color(4294967295),
      tertiaryFixed: Color(4285493909),
      onTertiaryFixed: Color(4294967295),
      tertiaryFixedDim: Color(4283849339),
      onTertiaryFixedVariant: Color(4294967295),
      surfaceDim: Color(4292271069),
      surfaceBright: Color(4294310653),
      surfaceContainerLowest: Color(4294967295),
      surfaceContainerLow: Color(4293915895),
      surfaceContainer: Color(4293586929),
      surfaceContainerHigh: Color(4293192171),
      surfaceContainerHighest: Color(4292797414),
    );
  }

  ThemeData lightMediumContrast() {
    return theme(lightMediumContrastScheme());
  }

  static ColorScheme lightHighContrastScheme() {
    return const ColorScheme(
      brightness: Brightness.light,
      primary: Color(4278199856),
      surfaceTint: Color(4278282109),
      onPrimary: Color(4294967295),
      primaryContainer: Color(4278208858),
      onPrimaryContainer: Color(4294967295),
      secondary: Color(4279117100),
      onSecondary: Color(4294967295),
      secondaryContainer: Color(4281353806),
      onSecondaryContainer: Color(4294967295),
      tertiary: Color(4280033342),
      onTertiary: Color(4294967295),
      tertiaryContainer: Color(4282204257),
      onTertiaryContainer: Color(4294967295),
      error: Color(4283301890),
      onError: Color(4294967295),
      errorContainer: Color(4287365129),
      onErrorContainer: Color(4294967295),
      surface: Color(4294310653),
      onSurface: Color(4278190080),
      onSurfaceVariant: Color(4280100136),
      outline: Color(4282139719),
      outlineVariant: Color(4282139719),
      shadow: Color(4278190080),
      scrim: Color(4278190080),
      inverseSurface: Color(4281086259),
      inversePrimary: Color(4291818239),
      primaryFixed: Color(4278208858),
      onPrimaryFixed: Color(4294967295),
      primaryFixedDim: Color(4278202941),
      onPrimaryFixedVariant: Color(4294967295),
      secondaryFixed: Color(4281353806),
      onSecondaryFixed: Color(4294967295),
      secondaryFixedDim: Color(4279840823),
      onSecondaryFixedVariant: Color(4294967295),
      tertiaryFixed: Color(4282204257),
      onTertiaryFixed: Color(4294967295),
      tertiaryFixedDim: Color(4280756809),
      onTertiaryFixedVariant: Color(4294967295),
      surfaceDim: Color(4292271069),
      surfaceBright: Color(4294310653),
      surfaceContainerLowest: Color(4294967295),
      surfaceContainerLow: Color(4293915895),
      surfaceContainer: Color(4293586929),
      surfaceContainerHigh: Color(4293192171),
      surfaceContainerHighest: Color(4292797414),
    );
  }

  ThemeData lightHighContrast() {
    return theme(lightHighContrastScheme());
  }

  static ColorScheme darkScheme() {
    return const ColorScheme(
      brightness: Brightness.dark,
      primary: Color(4287025642),
      surfaceTint: Color(4287025642),
      onPrimary: Color(4278203970),
      primaryContainer: Color(4278210143),
      onPrimaryContainer: Color(4289981439),
      secondary: Color(4289972948),
      onSecondary: Color(4280103995),
      secondaryContainer: Color(4281616978),
      onSecondaryContainer: Color(4291749616),
      tertiary: Color(4290888939),
      onTertiary: Color(4280954445),
      tertiaryContainer: Color(4282467429),
      onTertiaryContainer: Color(4292862207),
      error: Color(4294948011),
      onError: Color(4285071365),
      errorContainer: Color(4287823882),
      onErrorContainer: Color(4294957782),
      surface: Color(4279178262),
      onSurface: Color(4292797414),
      onSurfaceVariant: Color(4290758860),
      outline: Color(4287206038),
      outlineVariant: Color(4282402891),
      shadow: Color(4278190080),
      scrim: Color(4278190080),
      inverseSurface: Color(4292797414),
      inversePrimary: Color(4278282109),
      primaryFixed: Color(4289981439),
      onPrimaryFixed: Color(4278198055),
      primaryFixedDim: Color(4287025642),
      onPrimaryFixedVariant: Color(4278210143),
      secondaryFixed: Color(4291749616),
      onSecondaryFixed: Color(4278591013),
      secondaryFixedDim: Color(4289972948),
      onSecondaryFixedVariant: Color(4281616978),
      tertiaryFixed: Color(4292862207),
      onTertiaryFixed: Color(4279572791),
      tertiaryFixedDim: Color(4290888939),
      onTertiaryFixedVariant: Color(4282467429),
      surfaceDim: Color(4279178262),
      surfaceBright: Color(4281612860),
      surfaceContainerLowest: Color(4278849297),
      surfaceContainerLow: Color(4279704606),
      surfaceContainer: Color(4279967779),
      surfaceContainerHigh: Color(4280625965),
      surfaceContainerHighest: Color(4281349688),
    );
  }

  ThemeData dark() {
    return theme(darkScheme());
  }

  static ColorScheme darkMediumContrastScheme() {
    return const ColorScheme(
      brightness: Brightness.dark,
      primary: Color(4287354350),
      surfaceTint: Color(4287025642),
      onPrimary: Color(4278196512),
      primaryContainer: Color(4283341746),
      onPrimaryContainer: Color(4278190080),
      secondary: Color(4290236376),
      onSecondary: Color(4278327584),
      secondaryContainer: Color(4286420125),
      onSecondaryContainer: Color(4278190080),
      tertiary: Color(4291152111),
      onTertiary: Color(4279243569),
      tertiaryContainer: Color(4287336115),
      onTertiaryContainer: Color(4278190080),
      error: Color(4294949553),
      onError: Color(4281794561),
      errorContainer: Color(4294923337),
      onErrorContainer: Color(4278190080),
      surface: Color(4279178262),
      onSurface: Color(4294376446),
      onSurfaceVariant: Color(4291022032),
      outline: Color(4288455848),
      outlineVariant: Color(4286350472),
      shadow: Color(4278190080),
      scrim: Color(4278190080),
      inverseSurface: Color(4292797414),
      inversePrimary: Color(4278210400),
      primaryFixed: Color(4289981439),
      onPrimaryFixed: Color(4278195226),
      primaryFixedDim: Color(4287025642),
      onPrimaryFixedVariant: Color(4278205513),
      secondaryFixed: Color(4291749616),
      onSecondaryFixed: Color(4278195226),
      secondaryFixedDim: Color(4289972948),
      onSecondaryFixedVariant: Color(4280498497),
      tertiaryFixed: Color(4292862207),
      onTertiaryFixed: Color(4278849068),
      tertiaryFixedDim: Color(4290888939),
      onTertiaryFixedVariant: Color(4281349203),
      surfaceDim: Color(4279178262),
      surfaceBright: Color(4281612860),
      surfaceContainerLowest: Color(4278849297),
      surfaceContainerLow: Color(4279704606),
      surfaceContainer: Color(4279967779),
      surfaceContainerHigh: Color(4280625965),
      surfaceContainerHighest: Color(4281349688),
    );
  }

  ThemeData darkMediumContrast() {
    return theme(darkMediumContrastScheme());
  }

  static ColorScheme darkHighContrastScheme() {
    return const ColorScheme(
      brightness: Brightness.dark,
      primary: Color(4294311167),
      surfaceTint: Color(4287025642),
      onPrimary: Color(4278190080),
      primaryContainer: Color(4287354350),
      onPrimaryContainer: Color(4278190080),
      secondary: Color(4294311167),
      onSecondary: Color(4278190080),
      secondaryContainer: Color(4290236376),
      onSecondaryContainer: Color(4278190080),
      tertiary: Color(4294834687),
      onTertiary: Color(4278190080),
      tertiaryContainer: Color(4291152111),
      onTertiaryContainer: Color(4278190080),
      error: Color(4294965753),
      onError: Color(4278190080),
      errorContainer: Color(4294949553),
      onErrorContainer: Color(4278190080),
      surface: Color(4279178262),
      onSurface: Color(4294967295),
      onSurfaceVariant: Color(4294311167),
      outline: Color(4291022032),
      outlineVariant: Color(4291022032),
      shadow: Color(4278190080),
      scrim: Color(4278190080),
      inverseSurface: Color(4292797414),
      inversePrimary: Color(4278202170),
      primaryFixed: Color(4290834175),
      onPrimaryFixed: Color(4278190080),
      primaryFixedDim: Color(4287354350),
      onPrimaryFixedVariant: Color(4278196512),
      secondaryFixed: Color(4292078580),
      onSecondaryFixed: Color(4278190080),
      secondaryFixedDim: Color(4290236376),
      onSecondaryFixedVariant: Color(4278327584),
      tertiaryFixed: Color(4293191167),
      onTertiaryFixed: Color(4278190080),
      tertiaryFixedDim: Color(4291152111),
      onTertiaryFixedVariant: Color(4279243569),
      surfaceDim: Color(4279178262),
      surfaceBright: Color(4281612860),
      surfaceContainerLowest: Color(4278849297),
      surfaceContainerLow: Color(4279704606),
      surfaceContainer: Color(4279967779),
      surfaceContainerHigh: Color(4280625965),
      surfaceContainerHighest: Color(4281349688),
    );
  }

  ThemeData darkHighContrast() {
    return theme(darkHighContrastScheme());
  }


  ThemeData theme(ColorScheme colorScheme) => ThemeData(
     useMaterial3: true,
     brightness: colorScheme.brightness,
     colorScheme: colorScheme,
     textTheme: textTheme.apply(
       bodyColor: colorScheme.onSurface,
       displayColor: colorScheme.onSurface,
     ),
     scaffoldBackgroundColor: colorScheme.background,
     canvasColor: colorScheme.surface,
  );


  List<ExtendedColor> get extendedColors => [
  ];
}

class ExtendedColor {
  final Color seed, value;
  final ColorFamily light;
  final ColorFamily lightHighContrast;
  final ColorFamily lightMediumContrast;
  final ColorFamily dark;
  final ColorFamily darkHighContrast;
  final ColorFamily darkMediumContrast;

  const ExtendedColor({
    required this.seed,
    required this.value,
    required this.light,
    required this.lightHighContrast,
    required this.lightMediumContrast,
    required this.dark,
    required this.darkHighContrast,
    required this.darkMediumContrast,
  });
}

class ColorFamily {
  const ColorFamily({
    required this.color,
    required this.onColor,
    required this.colorContainer,
    required this.onColorContainer,
  });

  final Color color;
  final Color onColor;
  final Color colorContainer;
  final Color onColorContainer;
}
