import { Button, Card, Col, Form, Input, Row, Select } from "antd";
import { emotions } from "../utils/emotionConstants";
import { postReq } from "../_http/api";
import { useState, useRef } from "react";

export default function StartForm() {
  const videoRef = useRef(null);
  const [participantNumber, setParticipantNumber] = useState();
  const [emotion, setEmotion] = useState(emotions[0].value);
  const [video, setVideo] = useState(emotions[0].video);

  const onEndHandler = (e) => {
    videoRef.current.webkitExitFullscreen();
    postReq("stopWrite");
  };
  const handleBeginProgram = () => {
    postReq("start");
  };
  const handleEndProgram = () => {
    postReq("stop");
  };
  const handleStart = () => {
    console.log(participantNumber, emotion);
    const data = {
      subjectId: participantNumber,
      emotion: emotion,
    };
    postReq("startWrite", data);
    videoRef.current.play();
    videoRef.current.requestFullscreen();
  };

  return (
    <Row>
      <Col sm={24} md={12} lg={8}>
        <Card
          title={
            <div
              style={{
                height: "30vh",
                paddingTop: "10vh",
                whiteSpace: "normal",
                textAlign: "center",
                fontWeight: 700,
                fontSize: 17,
              }}
            >
              Human Emotion Detection with Electrocardiographic and
              Electroencephalographic Signals Using Machine Learning Techniques
            </div>
          }
          headStyle={{ borderBottom: 0 }}
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            width: "100%",
            height: "100vh",
            borderRadius: 0,
            border: "none",
            backgroundColor: "aliceblue",
          }}
          bodyStyle={{ flexGrow: 1 }}
          actions={[
            <Button
              type="primary"
              ghost
              danger
              style={{ width: "90%" }}
              onClick={handleEndProgram}
            >
              End Program
            </Button>,
            <Button
              type="primary"
              ghost
              style={{ width: "90%" }}
              onClick={handleBeginProgram}
            >
              Begin Program
            </Button>,
          ]}
        >
          <Form
            name="basic"
            labelWrap
            requiredMark={false}
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
          >
            <Form.Item
              label="Participant Number"
              name="participantnumber"
              rules={[
                {
                  required: true,
                  message: "Please enter participant number!",
                },
              ]}
            >
              <Input
                placeholder="Enter Participant Number"
                allowClear
                onChange={(event) => {
                  setParticipantNumber(event.target.value);
                }}
              />
            </Form.Item>
            <Form.Item
              label="Emotion Type"
              name="emotiontype"
              rules={[
                {
                  required: true,
                  message: "Please enter participant number!",
                },
              ]}
            >
              <Select
                placeholder="Select the Emotion"
                onChange={(event) => {
                  setEmotion(event);
                  const entry = emotions.filter(
                    (emotion) => emotion.value === event
                  );
                  console.log(entry[0].video);
                  setVideo(entry[0].video);
                }}
                allowClear
              >
                {emotions.map((emotion) => (
                  <Select.Option key={emotion.value} value={emotion.value}>
                    {emotion.label}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Row gutter={[5, 5]}>
              <Col span={24}>
                <Form.Item
                  wrapperCol={{}}
                  style={
                    {
                      //   paddingLeft: "33.5%",
                    }
                  }
                >
                  <Button
                    type="primary"
                    htmlType="submit"
                    onClick={handleStart}
                    style={{ width: "100%", marginTop: 40 }}
                  >
                    Start
                  </Button>
                </Form.Item>
              </Col>
            </Row>
          </Form>
        </Card>
        {/* </div> */}
      </Col>
      <Col sm={0} md={12} lg={16}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            minHeight: "100vh",
          }}
        >
          {emotions.map((emotionOfEmotions) => {
            if (emotionOfEmotions.value === emotion) {
              return (
                <video
                  width="480"
                  height="300"
                  controls
                  ref={videoRef}
                  onEnded={onEndHandler}
                >
                  <source src={video} type="video/mp4" />
                  Sorry, your browser doesn't support videos.
                </video>
              );
            }
            return null
          })}
        </div>
      </Col>
    </Row>
  );
}
