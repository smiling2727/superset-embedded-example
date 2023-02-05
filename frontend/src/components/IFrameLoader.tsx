import { Component } from "react";
import { embedDashboard } from "@superset-ui/embedded-sdk";
import './IFrameLoader.css'
import axios from "axios";

function fetchGuestTokenFromBackend(): Promise<string> {
    return new Promise<string>((resolve) => {
        console.log("====> Calling token!")
        axios.post("http://localhost:3000/fetchGuestToken").then((response) => {
            console.log(response.status);
        });
        resolve("mytoken");
    })
}

export class IFrameLoader extends Component {
    state = {
        isLoaded: false
    }

    componentDidMount() {
        this.setState({ isLoaded: true });
        embedDashboard({
            id: "825578f18-4f06-4e2f-b53c-d97a1a2d6ae8", // given by the Superset embedding UI
            supersetDomain: "http://localhost:8088",
            mountPoint: document.getElementById("my-superset-container")!, // any html element that can contain an iframe
            iframeAttributes: {"id": "my-test-frame", "className": "my-test-frame-class"},
            fetchGuestToken: () => fetchGuestTokenFromBackend(),
        });
    }

    render() {
        return <div id="my-superset-container" className="IFrameLoader"></div>
    }
}
