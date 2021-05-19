import React, { useState } from 'react';
import { Layout, AutoComplete, Button, Row, Col, Dropdown, Menu } from 'antd';
import { UserOutlined, DollarOutlined, FundViewOutlined, SearchOutlined } from '@ant-design/icons';
import './GeneralLayout.css';

const { Header, Content, Footer } = Layout;

const menu = (
	<Menu>
		<Menu.Item key="0"><a href='#'>My Account</a></Menu.Item>
		<Menu.Item key="1"><a href='#'>Settings</a></Menu.Item>
		<Menu.Divider />
		<Menu.Item key="3"><a href='#'>Log Out</a></Menu.Item>
	</Menu>
);

function GeneralLayout({ children, componentName }) {
	return (
		<Layout className={componentName || 'layout-general'}>
			<Navigation />
			<Content className='layout layout-content' style={{ padding: '50px' }}>
				{children}
			</Content>
			<Footer className='layout layout-footer' style={{ textAlign: 'center', backgroundColor: 'rgb( 255, 255, 255, 0 )' }}>Created with ❤️ on Planet Stocket</Footer>
		</Layout>
	);
}

function Navigation() {
	const [query, setQuery] = useState('');
	const [options, setOptions] = useState([]);

	const onSelect = () => { }
	const onSearch = () => { }
	const onChange = (value) => setQuery(value);

	return (
		<Header className='layout layout-header' style={{ zIndex: 1, width: '100%', background: 'rgb( 255, 255, 255, 0)' }}>
			<Row>
				<Col span={2} style={{ textAlign: 'center' }}>
					<FundViewOutlined />
				</Col>
				<Col span={4} offset={1} style={{ textAlign: 'center' }}>
					<AutoComplete
						value={query}
						options={options}
						style={{ width: '100%' }}
						onSelect={onSelect}
						onSearch={onSearch}
						onChange={onChange}
						placeholder={<Button type='link' size='small' icon={<SearchOutlined />} style={{ color: 'black' }}>Search something...</Button>}
						notFoundContent={<NoContentFound />}
					/>
				</Col>

				<Col span={4} offset={11} style={{ textAlign: 'center' }}>
					<Button type='link' size='large' icon={<DollarOutlined />} style={{ color: 'black' }} >
						111231.12
					</Button>
				</Col>

				<Col span={2} style={{ textAlign: 'center' }}>
					<Dropdown overlay={menu} placement='bottomCenter'>
						<Button type='link' size='large' icon={<UserOutlined />} style={{ color: 'black' }} />
					</Dropdown>
				</Col>
			</Row>
		</Header>
	)
}

function NoContentFound() {
	return (
		<>No content here</>
	)
}

export default GeneralLayout;