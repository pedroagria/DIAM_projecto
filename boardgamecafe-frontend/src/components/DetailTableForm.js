import React from "react";
import { Button, Form, FormGroup, Table } from "reactstrap";

class DetailTableForm extends React.Component {
    state = {
        pk: 0,
        name: "",
        capacity: 0,
        log_date_created: "",
        log_date_last_update: "",
    };

    componentDidMount() {
        if (this.props.table) {
            const { pk, name, capacity, log_date_created, log_date_last_update } = this.props.table;
            this.setState({ pk, name, capacity, log_date_created, log_date_last_update });
        }
    }

    closeModalTable = e => {
        e.preventDefault();
        this.props.toggle();
    };

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render() {
        return (
            <Form onSubmit={this.closeModalTable}>
                <FormGroup>
                    <b>Name:</b>
                    <p>{this.defaultIfEmpty(this.state.name)} </p>
                </FormGroup>
                <FormGroup>
                    <b>Capacity:</b>
                    <p>{this.defaultIfEmpty(this.state.capacity)} </p>
                </FormGroup>
                <FormGroup>
                    <b>Creation Date:</b>
                    <p>{this.defaultIfEmpty(this.state.log_date_created)} </p>
                </FormGroup>
                <FormGroup>
                    <b>Update Date:</b>
                    <p>{this.defaultIfEmpty(this.state.log_date_last_update)} </p>
                </FormGroup>
                <Button>Close</Button>
            </Form>
        );
    }
}

export default DetailTableForm;