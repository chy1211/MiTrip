import { Image } from 'react-native';

// Shown when a place has no photo (bundled asset, so it also works offline / on iOS without http).
export const PLACEHOLDER_PHOTO = Image.resolveAssetSource(require('../../assets/images/placeholder.png')).uri;

export const sortCategoryData = ['最新消息', '熱門商家'];
export const lswitch = ['我的旅程'];

export const date = ['9/30','10/1','10/2'];
export const num = ['1','2','3','4'];


export const categoriesData = [
    {
        title: '海洋',
        image: require('../../assets/images/ocean.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '山',
        image: require('../../assets/images/mountain.png'),
        star: '4.6',
        stats: '營業中'
    },
    {
        title: '城市',
        image: require('../../assets/images/city.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '夕陽',
        image: require('../../assets/images/sunset.png'),
        star: '4.6',
        stats: '營業中'
    },
    {
        title: '爬山',
        image: require('../../assets/images/hiking.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '沙灘',
        image: require('../../assets/images/beach.png'),
        star: '4.6',
        stats: '營業中'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    {
        title: '城',
        image: require('../../assets/images/forest.png'),
        star: '4.6',
        stats: '已打烊'
    },
    
    
]
export const destinationData = [
    {
        id: '1',
        title: '大阪三日遊',
        duration: '12 Days',
        distance: '400 KM',
        weather: '20 C',
        date: '2023/9/28',
        price: 1200,
        shortDescription: "Osaka Castle is a Japanese castle in Chūō-ku, Osaka, Japan. The castle is one of Japan's most famous landmarks.",
        longDescription: "Osaka Castle is a Japanese castle in Chūō-ku, Osaka, Japan. The castle is one of Japan's most famous landmarks and it played a major role in the unification of Japan during the sixteenth century of the Azuchi-Momoyama period.",
        image: require('../../assets/images/hotel.png')
    },
    {
        id: '2',
        title: '海岸',
        duration: '7 Days',
        distance: '450 KM',
        weather: '30 C',
        date: '2023/9/29',
        price: 3000,
        shortDescription: "The Itsukushima shrine is one of Japan's most popular tourist attractions.",
        longDescription: "Itsukushima Shrine is a Shinto shrine on the island of Itsukushima, best known for its 'floating' torii gate. It is in the city of Hatsukaichi in Hiroshima Prefecture in Japan, accessible from the mainland by ferry at Miyajimaguchi Station.",
        image: require('../../assets/images/island.png')
    },
    
    {
        id: '3',
        title: '塔',
        duration: '5 Days',
        distance: '299 KM',
        weather: '14 C',
        date: '2023/9/30',
        price: 1000,
        shortDescription: "Babusar Top is a mountain pass in Pakistan at the north of the 150 km long in beautiful Kaghan Valley",
        longDescription: "Babusar Pass or Babusar Top is a mountain pass in Pakistan at the north of the 150 km long Kaghan Valley, connecting it via the Thak Nala with Chilas on the Karakoram Highway. It is the highest point in Kaghan Valley that can be easily accessed by cars.",
        image: require('../../assets/images/city.png')
    },
    {
        id: '4',
        title: '寺',
        duration: '20 Days',
        distance: '604 KM',
        weather: '34 C',
        date: '2023/10/1',
        price: 400,
        shortDescription: "Todaiji is one of Japan's most famous and significant temples and a landmark of Nara.",
        longDescription: "Tōdai-ji is a Buddhist temple complex that was once one of the powerful Seven Great Temples, located in the city of Nara, Japan. Though it was originally founded in the year 738 CE, Tōdai-ji was not opened until the year 752 CE.",
        image: require('../../assets/images/forest.png')
    },
]