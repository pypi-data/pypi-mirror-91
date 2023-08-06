// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { FilterObjectArray } from "./components/taskpanes/ControlPanel/FilterCard";
import { SortDirection } from "./components/taskpanes/ControlPanel/SortCard";
import { AggregationType } from "./components/taskpanes/PivotTable/PivotTaskpane";


/*
  Contains a wrapper around a strongly typed object that simulates a web-api. 
*/
// TODO: add a class that takes a _send_ and a _receive_, and then has functions for each call of the API


// Max delay is the longest we'll wait for the API to return a value
const MAX_DELAY = 5000;
// How often we poll to see if we have a response yet
const RETRY_DELAY = 250;
const MAX_RETRIES = MAX_DELAY / RETRY_DELAY;


const getRandomId = (): string => {
    return '_' + Math.random().toString(36).substr(2, 9);
}

// NOTE: these have pythonic field names because we parse their JSON directly in the API
export interface SimpleImportSummary {
    step_type: 'simple_import';
    file_names: string[];
}
export interface RawPythonImportSummary {
    step_type: 'raw_python_import';
    python_code: string;
    new_df_names: string[];
}

export interface ImportSummaries {
    [key: string]: SimpleImportSummary | RawPythonImportSummary
}

/*
  The MitoAPI class contains functions for interacting with the Mito backend.

  TODO: we should move _all_ calls to send inside of this class, and 
  wrap them inside of stronger-typed functions. 
*/
export class MitoAPI {
    send: (msg: Record<string, unknown>) => void;
    unconsumedResponses: Record<string, unknown>[];

    constructor(send: (msg: Record<string, unknown>) => void) {
        this.send = send;
        this.unconsumedResponses = [];
    }

    /*
        The receive response function is a workaround to the fact that we _do not_ have
        a real API in practice. If/when we do have a real API, we'll get rid of this function, 
        and allow the API to just make a call to a server, and wait on a response
    */
    receiveResponse(response: Record<string, unknown>): void {
        this.unconsumedResponses.push(response);
    }

    /*
        Helper function that tries to get the response for a given ID, and returns
        the data inside the 'data' key in this response if it exists. 

        Returns undefined if it does not get a response within the set timeframe
        for retries.
    */
    getResponseData(id: string): Promise<unknown | undefined> {
    
        return new Promise((resolve) => {
            let tries = 0;
            const interval = setInterval(() => {
                // Only try at most MAX_RETRIES times
                tries++;
                if (tries > MAX_RETRIES) {
                    clearInterval(interval);
                    // If we fail, we return an empty response
                    return resolve(undefined)
                }

                // See if there is an API response to this one specificially
                const index = this.unconsumedResponses.findIndex((response) => {
                    return response['id'] === id;
                })
                if (index !== -1) {
                    // Clear the interval
                    clearInterval(interval);

                    const response = this.unconsumedResponses[index];
                    this.unconsumedResponses.splice(index, 1);
          
                    return resolve(response['data']); // return to end execution
                } else {
                    console.log("Still waiting")
                }
            }, RETRY_DELAY);
        })
    }

    /*
    Returns all the CSV files in the current folder as the kernel.
  */
    async getDataFiles(): Promise<string[]> {
        const id = getRandomId();

        this.send({
            'event': 'api_call',
            'type': 'datafiles',
            'id': id
        })

        const dataFiles = await this.getResponseData(id) as string[] | undefined;
    
        if (dataFiles == undefined) {
            return []
        }
        return dataFiles;
    }

    /*
        Import summaries are a mapping from step_idx -> import information for each of the 
        import steps in the analysis with the given analysisName.
    */
    async getImportSummary(analysisName: string): Promise<ImportSummaries> {
        const id = getRandomId();

        this.send({
            'event': 'api_call',
            'type': 'import_summary',
            'id': id,
            'analysis_name': analysisName
        })

        const importSumary = await this.getResponseData(id) as ImportSummaries | undefined;
    
        if (importSumary == undefined) {
            return {}
        }
        return importSumary;
    }


    /*
        Does a merge with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendMergeMessage(
        sheetOneIndex: number,
        sheetOneMergeKey: string,
        sheetOneSelectedColumns: string[],
        sheetTwoIndex: number,
        sheetTwoMergeKey: string,
        sheetTwoSelectedColumns: string[],
        /* 
            If you want to overwrite, you have to pass the ID of the the step that
            you want to overwrite. Not passing this argument, or passing an empty string,
            will result in no overwrite occuring (and a new stepID) being returned.
        */
        stepID?: string
    ): Promise<string> {
        // If this is overwriting a merge event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID == '') {
            stepID = getRandomId();
        }

        window.logger?.track({
            userId: window.user_id,
            event: 'button_merge_log_event',
            properties: {
                step_id: stepID,
                sheet_index_one: sheetOneIndex,
                merge_key_one: sheetOneMergeKey,
                selected_columns_one: sheetOneSelectedColumns,
                sheet_index_two: sheetTwoIndex,
                merge_key_two: sheetTwoMergeKey,
                selected_columns_two: sheetTwoSelectedColumns,
            }
        })

        this.send({
            event: 'edit_event',
            type: 'merge_edit',
            step_id: stepID,
            sheet_index_one: sheetOneIndex,
            merge_key_one: sheetOneMergeKey,
            selected_columns_one: sheetOneSelectedColumns,
            sheet_index_two: sheetTwoIndex,
            merge_key_two: sheetTwoMergeKey,
            selected_columns_two: sheetTwoSelectedColumns,
        })

        return stepID;
    }


    /*
        Does a pivot with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendPivotMessage(
        sheetIndex: number,
        pivotRows: string[],
        pivotCols: string[],
        values: Record<string, AggregationType>,
        stepID?: string
    ): Promise<string> {
        // If this is overwriting a pivot event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        window.logger?.track({
            userId: window.user_id,
            event: 'button_pivot_log_event',
            properties: {
                sheet_index: sheetIndex,
                pivot_rows: pivotRows,
                pivot_cols: pivotCols,
                values: values,
                step_id: stepID
            }
        })

        this.send({
            event: 'edit_event',
            type: 'pivot_edit',
            sheet_index: sheetIndex,
            pivot_rows: pivotRows,
            pivot_columns: pivotCols,
            values: values, 
            step_id: stepID
        });

        return stepID;
    }

    /*
        Does a filter with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendFilterMessage(
        sheetIndex: number,
        columnHeader: string,
        filters: FilterObjectArray,
        operator: 'And' | 'Or',
        stepID?: string    
    ): Promise<string> {
        // If this is overwriting a filter event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        window.logger?.track({
            userId: window.user_id,
            event: 'filter_log_event',
            properties: {
                sheet_index: sheetIndex,
                column_header: columnHeader,
                filters: filters,
                operator: operator
            }
        });

        this.send({
            event: 'edit_event',
            type: 'filter_column_edit',
            sheet_index: sheetIndex,
            column_header: columnHeader,
            operator: operator,
            filters: filters,
            step_id: stepID

        });

        return stepID;
    }

    /*
        Does a sort with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendSortMessage(
        sheetIndex: number,
        columnHeader: string,
        sortDirection: SortDirection,
        stepID?: string    
    ): Promise<string> {
        // If this is overwriting a sort event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        window.logger?.track({
            userId: window.user_id,
            event: 'sort_log_event',
            properties: {
                sheet_index: sheetIndex,
                column_header: columnHeader,
                sort_direction: sortDirection
            }
        });
    
        this.send({
            event: 'edit_event',
            type: 'sort_edit',
            sheet_index: sheetIndex,
            column_header: columnHeader,
            sort_direction: sortDirection,
            step_id: stepID
        });

        return stepID;
    }

    /*
        Does a sort with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendRenameColumn(
        sheetIndex: number,
        oldColumnHeader: string,
        newColumnHeader: string,
        stepID?: string    
    ): Promise<string> {
        // If this is overwriting a rename event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        window.logger?.track({
            userId: window.user_id,
            event: 'rename_column_event',
            properties: {
                sheet_index: sheetIndex,
                old_column_header: oldColumnHeader,
                new_column_header: newColumnHeader
            }
        });

        this.send({
            event: 'edit_event',
            type: 'rename_column_edit',
            sheet_index: sheetIndex,
            old_column_header: oldColumnHeader,
            new_column_header: newColumnHeader,
            stepID: stepID
        });

        return stepID;
    }
}