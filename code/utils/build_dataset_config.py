import json
import cv2

class ChannelConfig:
    
    use_event: bool
    input_channel: int
    
    def __init__(self, use_event: bool, input_channel: int) -> None:
        assert(input_channel >= 0 and input_channel < 3)
        self.input_channel = input_channel
        self.use_event = use_event



class ImageConfig:
    channels: [ChannelConfig]
    
    def __init__(self, channels: [ChannelConfig]) -> None:
           assert(len(channels) == 4)
           self.channels = channels
           
    def from_json(json:dict):
        channels = []
        for channel in json["channels"]:
            channels.append(ChannelConfig(channel["use_event"],channel["input_channel"]))
        return ImageConfig(channels)
    
    def build_frame(self, event_frame, rgb_frame):
        assert(event_frame.shape == rgb_frame.shape)
        result_frame = cv2.cvtColor(event_frame, cv2.COLOR_RGB2RGBA)

        for i in range(len(self.channels)):
            result_frame[:,:,i] = event_frame[:,:,self.channels[i].input_channel] if self.channels[i].use_event else rgb_frame[:,:,self.channels[i].input_channel]
        return result_frame
        
example_json = """{
   "channels":[
      {
         "use_event":false,
         "input_channel":0
      },
      {
         "use_event":false,
         "input_channel":1
      },
      {
         "use_event":false,
         "input_channel":2
      },
      {
         "use_event":true,
         "input_channel":0
      }
   ]
}"""




if __name__ == "__main__":
    json = json.loads(example_json)
    config = ImageConfig.from_json(json)

    event_frame = cv2.imread("./../tmp_event.png")
    rgb_frame = cv2.imread("./../tmp_mapped.png")
    print(event_frame.shape,rgb_frame.shape)
    test = config.build_frame(event_frame,rgb_frame)

    cv2.imwrite("test.png",test)
