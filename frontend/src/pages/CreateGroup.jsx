import React, { useEffect, useState } from "react";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import LinkButton from "../components/LinkButton";
import "../static/css/groups.css";
import InputField from "../components/InputField";
import { getCookie } from "../utils/cookieUtil";
import { parseJwt } from "../utils/tokenDecodeUtil";
import RegButton from "../components/RegButton";

const CreateGroup = () => {
  const [groupTitle, setGroupTitle] = useState("");
  const [groupSummery, setgroupSummery] = useState("");
  const [createById, setCreateById] = useState("");
  const [status, setStatus] = useState("Active");
  const [chatId, setChatId] = useState("");
  const [mainImage, setMainImage] = useState(
    "https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM="
  );
  const [currentChatIds, setCurrentChatIds] = useState([]);

  useEffect(() => {
    setCreateById(parseJwt(getCookie("access_token")).sub);

    const getGroupsChatIds = async () => {
      const response = await axios(SERVER_URL + "/groups/chat/ids", {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }).then((res) => {
        setCurrentChatIds(res.data.data);
      });
    };
    getGroupsChatIds();
  }, []);

  const addUserToGroup = async (groupId) => {
    const response = await axios.post(
      SERVER_URL + "/group/members/",
      {
        role: "admin",
        status: "active",
        user_id: createById,
        group_id: groupId,
      },
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
  };

  // const createNewChatId = (currentIds) =>{
  //   console.log(currentIds)
  //   setChatId((Number(currentIds[currentIds.length - 1]) + 1) + "");
  //   console.log((Number(currentIds[currentIds.length - 1]) + 1) + "")
  //   console.log("2")
  // }

  const createGroupHandle = async (e) => {
    e.preventDefault();
    //getGroupsChatIds();\

    function randomNumberInRange(min, max) {
      let randomNumber = Math.floor(Math.random() * (max - min + 1)) + min;
      while (currentChatIds.includes(randomNumber)) {
        randomNumber = Math.floor(Math.random() * (max - min + 1)) + min;
      }
      return randomNumber;
    }

    const getChatIds = await axios(SERVER_URL + "/groups/chat/ids", {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }).then(async (res) => {
      await axios
        .post(
          SERVER_URL + "/groups/",
          {
            title: groupTitle,
            summery: groupSummery,
            createdBy_id: createById,
            status: status,
            chatId: String(randomNumberInRange(1000, 9999)),
            mainImage: mainImage,
          },
          {
            headers: {
              authorization: "Bearer " + getCookie("access_token"),
            },
            Accept: "application/json",
            "Content-Type": "application/json",
          }
        )
        .then((res2) => {
          addUserToGroup(res2.data.data.id);
        });
    });

    console.log("2");
  };

  // const createGroup = async () => {
  //   const response = await axios(SERVER_URL + "/groups/chat/ids", {
  //     headers: {
  //       Accept: "application/json",
  //       "Content-Type": "application/json",
  //     },
  //   })
  //     .then((response) => {
  //       setCurrentChatIds(response.data.data);
  //       console.log(currentChatIds)
  //       console.log("object")
  //       return response.data.data;
  //     })
  //     .then(async (currentChatIds) => {
  //       e.preventDefault();
  //       await axios.post(
  //         SERVER_URL + "/groups/",
  //         {
  //           title: groupTitle,
  //           summery: groupSummery,
  //           createdBy_id: createById,
  //           status: status,
  //           chatId: String(
  //             Number(currentChatIds[currentChatIds.length - 1] + 1)
  //           ),
  //           mainImage: mainImage,
  //         },
  //         {
  //           headers: {
  //             authorization: "Bearer " + getCookie("access_token"),
  //           },
  //           Accept: "application/json",
  //           "Content-Type": "application/json",
  //         }
  //       );
  //     })
  //     .then(() => addUserToGroup(response.data.data.id));
  // };

  return (
    <div>
      <form onSubmit={createGroupHandle} className="row g-3">
        <div className="col-md-6">
          {InputField("Title", "inputTitle", "this title", "text", (e) =>
            setGroupTitle(e.target.value)
          )}
        </div>
        <div className="col-md-6">
          {InputField(
            "Summery",
            "inputSummery",
            "describe shortly about the group",
            "text",
            (e) => setgroupSummery(e.target.value)
          )}
        </div>
        <div className="col-12">
          {InputField(
            "Main image",
            "inputMainImage",
            "Image url",
            "text",
            (e) => setMainImage(e.target.value)
          )}
        </div>
        <div className="col-12">
          {RegButton("Create", "submit")}
          {/* <button type="submit">Create</button> */}
        </div>
      </form>
    </div>
  );
};

export default CreateGroup;
