import React, { useEffect, useState } from "react";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import LinkButton from "../components/LinkButton";
import "../static/css/groups.css";

const Groups = () => {
  const [groups, setGroups] = useState([]);
  const [groupIds, setGroupIds] = useState([]);
  const [users, setUsers] = useState("");
  const [groupSearchValue, setGroupSearchValue] = useState("");

  useEffect(() => {
    const server_data = async () => {
      const response = groupSearchValue
        ? await axios(SERVER_URL + "/groups/search/" + groupSearchValue, {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          })
        : await axios(SERVER_URL + "/groups/", {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          });
      setGroups(response.data.data);
      setGroupIds(response.data.groups_ids);
      console.log(response.data.data);
    };
    server_data();
  }, [groupSearchValue]);

  return (
    <div className="mainContainer">
      <div className="group-search">
        <input
          id="group-search"
          className="group-search-input"
          type="text"
          placeholder="Group title"
          autoComplete={"false"}
          onChange={(e) => {
            setGroupSearchValue(e.target.value);
          }}
        ></input>
        <label className="input-label" htmlFor="group-search">
          Search{" "}
        </label>
      </div>
      <h1 className="main-title">Groups</h1>
      <div className="groups-view">
        {groups ? (
          groups.map((group, ind) => (
            <div className="single-group" key={ind}>
              <div>
                <img
                  className="group-image"
                  src={group.mainImage}
                  alt="https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM="
                />
              </div>
              <div className="card-content">
                <h2>{group.title}</h2>
                <p>{group.summery}</p>
                {LinkButton("Visit", groupIds[ind])}
              </div>
            </div>
          ))
        ) : (
          <div>
            <h2>No groups were found</h2>
          </div>
        )}
      </div>
      <div>
        <div>{LinkButton("Create Group", "/creategroup")}</div>
      </div>
    </div>
  );
};

export default Groups;
