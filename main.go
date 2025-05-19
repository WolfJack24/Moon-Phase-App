package main

import (
	"embed"
	"log"

	"github.com/wailsapp/wails/v3/pkg/application"
)

//go:embed all:frontend/dist
var assets embed.FS
var payloadservice = &PayloadService{}
var colourservice = &ColourService{}

func main() {
	app := application.New(application.Options{
		Name:        "MoonPhaseApp",
		Description: "A Wails application to display the moon phase",
		Services: []application.Service{
			application.NewService(payloadservice),
			application.NewService(colourservice),
		},
		Assets: application.AssetOptions{
			Handler: application.AssetFileServerFS(assets),
		},
		Mac: application.MacOptions{
			ApplicationShouldTerminateAfterLastWindowClosed: true,
		},
	})

	app.NewWebviewWindowWithOptions(application.WebviewWindowOptions{
		Title:         "Moon Phase App", // TODO: Need a better name
		Width:         511,
		Height:        351,
		URL:           "/",
		DisableResize: true,
		Mac: application.MacWindow{
			InvisibleTitleBarHeight: 50,
			Backdrop:                application.MacBackdropTranslucent,
			TitleBar:                application.MacTitleBarHiddenInset,
		},
		BackgroundColour: application.RGBA(colourservice.HexToRGB(WindowBackground)),
	})

	err := app.Run()

	if err != nil {
		log.Fatal(err)
	}
}
