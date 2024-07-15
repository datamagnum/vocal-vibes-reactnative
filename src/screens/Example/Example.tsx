import { useEffect, useState } from 'react';
import {
	View,
	ActivityIndicator,
	Text,
	TouchableOpacity,
	ScrollView,
	Alert,
} from 'react-native';
import i18next from 'i18next';
import { useTranslation } from 'react-i18next';
import { useQuery } from '@tanstack/react-query';

import { ImageVariant } from '@/components/atoms';
import { Brand } from '@/components/molecules';
import { SafeScreen } from '@/components/template';
import { useTheme } from '@/theme';

import { isImageSourcePropType } from '@/types/guards/image';

import SendImage from '@/theme/assets/images/send.png';
import ColorsWatchImage from '@/theme/assets/images/colorswatch.png';
import TranslateImage from '@/theme/assets/images/translate.png';

function Example() {
	const { t } = useTranslation(['example', 'welcome']);
	const [currentId, setCurrentId] = useState(-1);

	return (
		<SafeScreen>
			<ScrollView>
				<View><Text>Hello</Text></View>
			</ScrollView>
		</SafeScreen>
	);
}

export default Example;
