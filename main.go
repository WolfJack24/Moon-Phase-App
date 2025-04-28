package main

import (
	"embed"
	"log"

	"github.com/wailsapp/wails/v3/pkg/application"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	app := application.New(application.Options{
		Name: "MoonPhaseApp",
		Description: "A Wails application to display the moon phase",
		Services: []application.Service{
			application.NewService(&PayloadService{}),
		},
		Assets: application.AssetOptions{
			Handler: application.AssetFileServerFS(assets),
		},
		Mac: application.MacOptions{
			ApplicationShouldTerminateAfterLastWindowClosed: true,
		},
	})

	app.NewWebviewWindowWithOptions(application.WebviewWindowOptions{
		Title: "Moon Phase App",
		Width: 500,
		Height: 351,
		URL: "/",
		DisableResize: true,
		Mac: application.MacWindow{
			InvisibleTitleBarHeight: 50,
			Backdrop: application.MacBackdropTranslucent,
			TitleBar: application.MacTitleBarHiddenInset,
		},
		BackgroundColour: application.NewRGB(27, 38, 54),
	})

	err := app.Run()

	if err != nil {
		log.Fatal(err)
	}
}
