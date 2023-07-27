import { Button, Card, Col, Form, Input, Row, Select } from "antd";
import { emotions } from "../utils/emotionConstants";
import backgroundImage from "../images/background.webp";
import { postReq } from "../_http/api";
import { useState } from "react";

export default function StartForm() {
  const [participantNumber, setParticipantNumber] = useState();
  const [emotion, setEmotion] = useState("");

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
  };
  const handleStop = () => {
    postReq("stopWrite");
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
                value={emotion}
                onChange={(event) => {
                  setEmotion(event);
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
              <Col span={12}>
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
                    danger
                    onClick={handleStop}
                    style={{ width: "80%", marginLeft: 40, marginTop: 40 }}
                  >
                    Stop
                  </Button>
                  {/* <Button
                  type="primary"
                  htmlType="submit"
                  style={{ width: "100%", backgroundColor: "green" }}
                >
                  Begin
                </Button> */}
                </Form.Item>
              </Col>
              <Col span={12}>
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
                    style={{ width: "80%", marginLeft: 40, marginTop: 40 }}
                  >
                    Start
                  </Button>
                  {/* <Button
                  type="primary"
                  htmlType="submit"
                  style={{ width: "100%", backgroundColor: "green" }}
                >
                  Begin
                </Button> */}
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
            backgroundImage: `url(${backgroundImage})`,
          }}
        ></div>
      </Col>
    </Row>
  );
}
