import React, { Component } from "react";
import { Table } from "reactstrap";
import DetailTableModal from "./DetailTableModal";

class TableList extends Component {
    render() {
        const tables = this.props.tables;
        return (
            <Table light>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Capacity</th>
                        <th>Creation Date</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {!tables || tables.length <= 0 ? (
                        <tr>
                            <td colSpan="6" align="center">
                                <b>The are no tables to show</b>
                            </td>
                        </tr>
                    ) : (
                        tables.map(table => (
                            <tr key={table.pk}>
                                <td>{table.name}</td>
                                <td>{table.capacity}</td>
                                <td>{table.log_date_created}</td>
                                <td align="center">
                                    <DetailTableModal
                                        create={false}
                                        table={table}
                                        resetState={this.props.resetState}
                                    />
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </Table>
        );
    }
}

export default TableList;