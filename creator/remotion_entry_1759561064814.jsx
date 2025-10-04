import { registerRoot, Composition } from "remotion";
import { Video } from "./src/Video";

const fps = 30;
const width = 1080;
const height = 1920;

// The actual props will be passed via inputProps in renderMedia
export const RemotionRoot = () => {
  return (
    <Composition
      id="Video"
      component={Video}
      fps={fps}
      width={width}
      height={height}
      durationInFrames={3049}
      defaultProps={{
        images: ["assets/images/image_1.png","assets/images/image_3.png","assets/images/image_4.png","assets/images/image_5.png","assets/images/image_7.png","assets/images/image_8.png","assets/images/image_9.png","assets/images/image_12.png","assets/images/image_13.png","assets/images/image_15.png","assets/images/image_17.png","assets/images/image_18.png","assets/images/image_19.png","assets/images/image_20.png","assets/images/image_22.png","assets/images/image_23.png","assets/images/image_24.png","assets/images/image_25.png","assets/images/image_26.png","assets/images/image_27.png"],
        audio: "assets/audio/Untitled.wav",
        durationSeconds: 101.611,
      }}
    />
  );
};

registerRoot(RemotionRoot);
