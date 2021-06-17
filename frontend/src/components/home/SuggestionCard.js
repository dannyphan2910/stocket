import { Collapse } from 'antd';
import React from 'react';
import GeneralCard from '../shared/GeneralCard';

function SuggestionCard(props) {
    return (
        <Collapse ghost>
            <GeneralCard style={{ minHeight: '200px' }}>
            </GeneralCard>
        </Collapse>
    );
}

export default SuggestionCard;