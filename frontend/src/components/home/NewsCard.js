import React from 'react';
import { Collapse } from 'antd';
import GeneralCard from '../shared/GeneralCard';

function NewsCard(props) {
    return (
        <Collapse ghost>
            <GeneralCard style={{ minHeight: '200px' }}>
            </GeneralCard>
        </Collapse>
    );
}

export default NewsCard;