using System;

namespace MoonPhaseApp;

public static class Constants
{
    public static readonly string DirectoryPath = Environment.CurrentDirectory;
    public static readonly string AssetsPath = $"{DirectoryPath}/Assets";
    public static readonly string FileDir = $"{DirectoryPath}/Secret";
    public static readonly string FileName = $"{FileDir}/Secret.bin";

    // Format
    public static readonly string DefualtFormat = "png";

    // Style
    public static readonly string DefaultMoonstyle = "default";
    public static readonly string DefaultBackgroundStyle = "stars";
    public static readonly string DefaultBackgroundColour = "black";
    public static readonly string DefaultHeadingColour = "white";
    public static readonly string DefaultTextColour = "white";

    // Observer
    public static readonly double DefaultLatitude = 6.56774;
    public static readonly double DefaultLongitude = 79.88956;
    public static readonly string DefaultDate = "2024-07-18";

    // View
    public static readonly string DefaultType = "portrait-simple";
    public static readonly string DefaultOrientation = "south-up";
}