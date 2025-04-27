export namespace main {
	
	export class Payload {
	    Format: string;
	    MoonStyle: string;
	    BackgroundStyle: string;
	    BackgroundColour: string;
	    HeadingColour: string;
	    TextColour: string;
	    Latitude: number;
	    Longitude: number;
	    Date: string;
	    Type: string;
	    Orientation: string;
	
	    static createFrom(source: any = {}) {
	        return new Payload(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Format = source["Format"];
	        this.MoonStyle = source["MoonStyle"];
	        this.BackgroundStyle = source["BackgroundStyle"];
	        this.BackgroundColour = source["BackgroundColour"];
	        this.HeadingColour = source["HeadingColour"];
	        this.TextColour = source["TextColour"];
	        this.Latitude = source["Latitude"];
	        this.Longitude = source["Longitude"];
	        this.Date = source["Date"];
	        this.Type = source["Type"];
	        this.Orientation = source["Orientation"];
	    }
	}

}

