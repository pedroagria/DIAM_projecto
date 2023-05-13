import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import TableList from "./TableList";
import axios from "axios";
import { API_URL_TABLES } from "../constants";

class Home extends Component {
    state = {
        tables: [],
    };

    componentDidMount() {
        this.resetState();
    }

    getTables = () => {
        axios.get(API_URL_TABLES).then(res => this.setState({ tables: res.data }));
    };

    resetState = () => {
        this.getTables();
    };

    render(){
        return(
            <Container style={{ marginTop: "20px"}}>
                <Row>
                    <Col>
                        <TableList
                            tables={this.state.tables}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default Home;