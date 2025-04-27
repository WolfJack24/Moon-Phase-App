package main

import (
	"context"
)

type Payload struct {
	// Format
	Format string

	// Style
	MoonStyle string
	BackgroundStyle string
	BackgroundColour string
	HeadingColour string
	TextColour string

	// Observer
    Latitude float32
    Longitude float32
    Date string

    // View
    Type string
    Orientation string
}

type App struct {
	ctx context.Context
}

func NewApp() *App {
	return &App{}
}

func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

func (a *App) CreatePayload() Payload {
	return Payload {
		Format: "png",
		MoonStyle: "default",
		BackgroundStyle: "stars",
		BackgroundColour: "black",
		HeadingColour: "white",
		TextColour: "white",
		Latitude: 6.56774,
		Longitude: 79.88956,
		Date: "2024-07-18",
		Type: "portrait-simple",
		Orientation: "south-up",
	};
}