import pytest
import parse

@pytest.fixture()
def simple():
    return 'A. E. UHE, by Frederick H. Martens. (Little biographies: series 1, Musicians) © 30Dec22, A695089. R59809, 17Mar50, Breitkopf Publications, inc., successor to Breitkopf & Haertel, inc. (PWH)'


@pytest.fixture()
def simple_auth_title():
    return 'ACTUAL BUSINESS ENGLISH, by P. H. Deffendall. © 1Aug22, A681161. R60449, 5Apr50, P. H. Deffendall (A)'


@pytest.fixture()
def f1_numbered_edition():
    return 'THE ART OF ANESTHESIA, by Paluel J. Flagg. 3d rev. ed. © 18Oct22, A692169. R56339, 23Dec49, Paluel J. Flagg (A)'


@pytest.fixture()
def f1_reg_pairs():
    return "ABBOTT'S DIGEST OF ALL THE NEW YORK REPORTS. Apr., July, Oct., Dec. 1922. © 31May22, B528574; 24Aug22, B548911; 2Dec22, B553698; 2Mar23, B571736. R61801, R61806, R61808, R61815, 28Apr50, The Lawyers Co-operative Publishing Co. (PCW)"


@pytest.fixture()
def one_part_ren_mixed():
    return 'AMERICAN LAW REPORTS ANNOTATED. Cumulative index, v. 16-18, 16-19, 16-20, 22-23. Indexes to cases and notes combined. © 13Jul22, A683889; 6Sep22, A683890; 23Oct22, A683891; 23Apr23, A704483. R61784-61786, R61796, 28Apr50, The Lawyers Co-operative Publishing Co. (PCW) & Bancroft-Whitney Co. (PCW)'


@pytest.fixture()
def many_reg_dates_one_reg_num():
    return 'CATHERINE, comédie en 4. actes de Henri Lavedan. (In Les Annales, nos. 2061-2064) © 24Dec22, 31Dec22, 7Jan23, 14Jan23, D63725. R61029, 17Apr50, Mme veuve Henri Lavedan, née Pauline Auguez (W)'


@pytest.fixture()
def one_date_list_of_regnums():
    return 'SOUTH CAROLINA DIGEST, 1783-1886. v. 1-2. © 2Dec22, A698474, A698473. R57358-57359, 16Jan50, West Publishing Co. (PWH)'


@pytest.fixture()
def date_range_one_regnum():
    return "REINE DE TANGO, grand roman, inédit par Marcel Priollet. 24 installments. (In Echo du nord, Lille) © 10Sep22-18Feb23, AF22373. R61026, 14Apr50, Marcel Priollet (A)"


@pytest.fixture()
def one_regnum_multiple_renewals():
    return "WISDOM'S DAUGHTER, being the autobiography of She-Who-Must-Be-Obeyed, by H. Rider Haggard; illus. by A. E. Jackson. Pub. in England in Hutchinson's magazine. Mar.-Dec. 1922. © 9Mar23 (pub. abroad 20Feb22, AI-4391; 23Mar22, AI-4440; 20Apr22, AI-4472; 23May22, AI-4534; 22Jun22, AI-4583; 18Jul22, AI-4625; 24Aug22, AI-4674; 16Sep22, AI-4718; 13Oct22, AI-4763; 13Nov22, AI-4820), A698959. R59879-59888, 10Mar50, Lilias Margitson Rider Haggard (C) & Angela Agnes Rider Haggard (C)"

@pytest.fixture()
def single_interim_pub():
    return "ADDRESS, by Rudyard Kipling, at the annual dinner of the Royal College of Surgeons, Feb. 14, 1923. Pub. in England in the Morning post, Feb. 15, 1923, as The mystery of man's triumphs of surgery. © 27Mar23 (pub. abroad 15Feb23, AI-4905), A704583. R60233, 28Mar50, Elsie Bambridge (C)"


@pytest.fixture()
def interim_pub_date_only():
    return "THE COOK'S WEDDING AND OTHER STORIES, from the Russian of Anton Chekhov. Constance Garnett, translator. © 21Mar22 (pub. abroad 2Feb22), A659245. R59404, 13Mar50, David Garnett (C)"


@pytest.fixture()
def multiple_interim_pub():
    return "AND THE DEAD SPAKE; AND THE HORROR-HORN, by E. F. Benson. Pub. in England in Hutchinson's magazine, Sept.-Oct. 1922, under titles \"The horror-horn\" and \"And the dead spake\"; illustrated by \"Blam.\" © 1Mar23, (pub. abroad 24Aug22, 16Sep22, AI-4680, AI-4725), A696722. R59139, 3Mar50, Kenneth Stewart Patrick McDowell (NK)"


@pytest.fixture()
def simple_two_parts():
    return "AN ADVANCED COURSE OF INSTRUCTION IN CHEMICAL PRINCIPLES, by Arthur A. Noyes and Miles S. Sherrill. Complete ed.|© 16May22, A674144. R59672, 20Mar50, Clement Gould Noyes (NK)"


@pytest.fixture()
def two_part_preceding_info():
    return 'LES THIBAULT, par Roger Martin du Gard.|t. 1: Le cahier gris. © 1May22, AF19918. R61349, 24Apr50, Roger Martin du Gard (A)'


@pytest.fixture()
def two_part_bracket_comment():
    return 'COL. WM. F. CODY, by Robert Lindneux.|[Buffalo Bill, astride white horse; horse standing on brow of hill north-west of Cody, overlooking the town; Cedar and Rattlesnake mountains in background] © 18Mar22, G65236. R59553, 9Mar50, Robert Lindneux (A)'


@pytest.fixture()
def chiastic_three_part():
    return "DESERT RUBAIYAT, by Arthur C. Train.|(In McCall's magazine) © Helen C. Train (W)|June 1923 issue. © 10May23, B576564. R69499, 8Nov50."


@pytest.fixture()
def renewal_id_range():
    return 'ADVENTURES OF DOCTOR DOLITTLE, by Hugh Lofting. (In the New York tribune, Dec. 24-31, 1922) © 24Dec22, B542207; 25Dec22, B542208; 26Dec22, B542209; 27Dec22, B542210; 28Dec22, B542211; 29Dec22, B542212; 30Dec22, B542213; 31Dec22, B542214. R63718-63725, 23Jun50, Josephine Lofting (W)'


@pytest.fixture()
def chiastic_id_range():
    return "AINSLEE'S. © Street & Smith Publications, inc. (PCW)|v. 50, nos. 4-5, Dec. 1922-Jan. 1923. © 15Nov22, 15Dec22, B551759, B567153. R56538-56539, 30Dec49."


@pytest.fixture()
def new_matter():
    return 'AMERICAN POCKET MEDICAL DICTIONARY; W. A. Newman Dorland, editor. 12th ed., rev. © on new matter; 22May22, A661865. R59332, 7Mar50, W. B. Saunders Co. (PWH)'


@pytest.fixture()
def class_code_phrase():
    return "THE FAIRY BOOK, by Dinah Maria Mulock [Craik] Illus. by Louis Rhead. © on illus.; 6Dec22, A692448. R60242, 30Mar50, Stephen Yates (NK of Louis Rhead)"


@pytest.fixture()
def missing_class_code():
    return "FRANKLIN'S HOMECOMING, High Street wharf, Philadelphia, by Jean Leon Gerome Ferris. [Group picture, ship at center] © 28Mar23, G68152. R63588, 23Jun50, Ernest N. Ryder, administrator d.b.n.c.t.a. estate of author."


@pytest.fixture()
def patent_office():
    return 'AVANTI. (Cigars) Date of publication 5Nov21, Date of registration in Patent Office 2May22, Label 24313. R57688, 25Jan50, Parodi Cigar Co. of N. Y. (P)'


@pytest.fixture()
def ny_herald():
    return 'NEW YORK HERALD. © New York Herald Tribune, inc. (PCW)|v. 86, no. 336-v. 87, no. 1, Aug. 1-31, 1922. © 1Aug22, 2Aug22, 3Aug22, 4Aug22, 5Aug22, 6Aug22, 7Aug22, 8Aug22, 9Aug22, 10Aug22, 11Aug22, 12Aug22, 13Aug22, 14Aug22, 15Aug22, 16Aug22, 17Aug22, 18Aug22, 19Aug22, 20Aug22, 21Aug22, 22Aug22, 23Aug22, 24Aug22, 25Aug22, 26Aug22, 27Aug22, 28Aug22, 29Aug22, 30Aug22, 31Aug22, B541697-541727. R65000-65030, 28Jul50.'


@pytest.fixture()
def pub_abroad_at_end():
    return 'ORCZY, EMMUSKA, baroness. The Honourable Jim. © 28Mar24, A778636. R76900-R76910, 11Apr51; R77709, 19Apr51; R76911-R76915, 11Apr51; John Montague Orczy-Barstow (C) Pub. abroad in installments in the British weekly, Oct. 11, 1923-Jan. 31, 1924. Chap. 1-2. © 11Oct23, AI-5562.'


@pytest.fixture()
def format_two():
    return 'A.L.R. CUMULATIVE INDEX-DIGEST. Vol.5, covering v.126-150. © 5Oct44; A183343. Lawyers Co-operative Pub. Co. & Bancroft-Whitney Co. (PWH); 16Mar72; R525069.'


@pytest.fixture()
def two_part_format_two():
    return 'ABBETT, ROBERT W.|Engineering contracts and specifications. © 8Jan45; A185390. Robert W. Abbett (A); 17Jan72; R523485.'


@pytest.fixture()
def format_two_two_cc():
    return 'ABBOTT, AUSTIN.|Digest of all the New York reports. Third supplement, 1918-1924. Vol. 4-5. © Lawyers Co-operative Pub. Co. (PCW)|v. 4. © 3May26; A890950. 21Apr54; R129485.'


@pytest.fixture()
def format_two_3_part_cc_one_three():
    return 'THE NEW YORK TIMES INDEX. Joseph C. Gephart, editor. © New York Times Co. (PWH)|v.32, no.|6. © 21Aug44; AA463212. 26Jan72; R522151.'


@pytest.fixture()
def format_two_2_part_2_cc():
    return 'AMERICAN LAW REPORTS, ANNOTATED. © Lawyers Co-operative Pub. Co. & Bancroft-Whitney Co. (PWH) Vol.|148. © 20Mar44; A179593. 6Mar72; R524719.'


@pytest.fixture()
def f2_four_parts():
    return 'CALIFORNIA. DISTRICT COURTS OF APPEAL.|Advance California appellate reports. J. O. Tucker, editor. © Bancroft-Whitney Co. (PWH)|v. 5, no.|27. © 14Jul44; AA462954. 14Jun72; R530779.'


@pytest.fixture()
def f2_multiple_renewals():
    return 'BEMELMANS, LUDWIG.|The blue Danube. (In Town & country, Mar.--Apr. 1945) © 1Mar45, B667185; 1Apr45, B674769. Madeleine Bemelmans (W) & Barbara Marciano (C); 7Apr72; R527187-527188.'


@pytest.fixture()
def f2_on_translation():
    return 'CIANO, GALEAZZO, CONTE.|The Ciano diaries, by Count Galeazzo. (In Chicago daily news) Appl. author: Countess Edda Ciano, employer for hire. © on translation; Countess Edda Mussolini Ciano (PWH)|© 18Jun45; B673449. 22Sep72; R537443.'


@pytest.fixture()
def f2_regnum_ranges():
    return 'WILLIAM J.|Federal practice, jurisdiction & procedure, civil and criminal, with forms. Assisted by George C. Thorpe. Vol.5-11. © 2Feb31, A35829-35830; 3Feb31, A35831, A35816; 4Feb31, A35817-35818; 5Feb31, A35819. William J. Hughes, Jr. (C); 7May58; R214419-214425.'
    

@pytest.fixture()
def label_id():
    return 'BEN-GAY. (Medicinal preparation for rheumatism, gout and neuralgia) © 5Apr22, Label 24762. R60358, 3Apr50, Bengue, inc. (P)'


@pytest.fixture()
def regnum_af():
    return "LE COEUR CAMBRIOLÉ, une histoire éponvantable, la Hache d'or, par Gaston Leroux. © 18Oct22, AF21459. R57493, 19Jan50, Mme. vve. Gaston Leroux, née Jeanne-Madeleine Cayatte (W)"


@pytest.fixture()
def regnum_aa():
    return "LE CÔTÉ DE GUERMANTES [et] SODOME ET GOMORRHE II, par Marcel Proust. (His A la recherche du temps perdu, 2-3, t. 5) 3 v. © 1May22, AA19985. R61350, 24Apr50, Mme. Gérard Mante, née Sivy Proust (NK)"


@pytest.fixture()
def regnum_ai():
    return 'CROMPTON, RICHMAL.|The house. © 26Mar26; AI-8054. Richmal Crompton (A); 24Feb54; R125974.'


@pytest.fixture()
def regnum_a5():
    return 'ADAMSON, HAROLD.|Bring on the girls. Words by Harold Adamson. © 9Feb45; A5-135834. Famous Music Corp. (PWH); 17Mar72; R524510.'


@pytest.fixture()
def regnum_b5():
    return 'THE NEWLYWEDS, by Charles McManus. (In the New York journal, May 14, 1923) © 14May23, B5-14369. R63445, 1Jun50, King Features Syndicate, inc. (PWH)'


@pytest.fixture()
def regnum_dp():
    return 'ANNA KARENINA, Oper In 3 Aufzügen (vier Bildern) von Alexandar Goth, Deutsch von Hans Liebstoeckl. Musik von Jeno Hubay, Op.112. klavierauszug von A. Szikla. © 7Nov22, DP220. R67406, 15Sep50, Andor v, Hubay-Cebrian (C), Tibor v. Hubay-Cebrian (C)'


@pytest.fixture()
def regnum_c():
    return 'THE AUCTIONEER OFFERING A BARREL OF FUN, a monologue by George Heather. © 15Dec22, C2352. R62366, 19May50, George Heather (A)'


@pytest.fixture()
def regnum_f():
    return 'ATLAS OF HUMBOLDT COUNTY, CALIFORNIA, by Belcher Abstract and Title Company. © Belcher Abstract & Title Co. (PWH)|Sheet no. 9. © 26Jan22, F37697. R57136, 16Jan50.'


@pytest.fixture()
def regnum_i():
    return 'DENTAL CHART SHOWING DRAWING OF TEETH, by Harry M. Chandler. © 8May22, I6581. R59420, 14Mar50, Harry M. Chandler (A)'


@pytest.fixture()
def regnum_iu():
    return '"FROGIKIN" DRAWINGS to show internal structure of frog, by Ada Louise Weckel. © 28Sep23, IU8397. R70130, 15Nov50, Clara Weckel Stephenson (NK)'


@pytest.fixture()
def regnum_j():
    return 'HEAD OF CHRIST IN BAS RELIEF, by W. Clark Noble. © 28Dec22, J259120. R72044, 27Dec50, Emilie Bleecher Noble (W)'


@pytest.fixture()
def regnum_k():
    return 'AND SO, AS WE SAID BEFORE; by [International Feature Service, inc., as employer for hire of George] Herriman. (In Krazy Kat) © 1Jul22, K167207. R61953, 3May50, King Features Syndicate, inc. (PWH)'


@pytest.fixture()
def regnum_l():
    return "ADAM'S RIB, a photoplay in ten reels, by Famous Players-Lasky Corp. © 7Feb23, L18658. R58624, 17Feb50, Paramount Pictures Corp. (PWH)"


@pytest.fixture()
def regnum_print():
    return 'BRILLO MAKES OLD ALUMINUM UTENSILS NEW. (Cleaning end polishing outfits) © 1Feb22, Print 6158. R57734, 25Jan50, Brillo Manufacturing Co., inc. (P)'


@pytest.fixture()
def f2_simplest():
    return 'ABBOTT, AUSTIN.|Digest of all the New York reports, 1925. © 14Aug26; A901544. Lawyers Co-operative Pub. Co. (PCW); 21Apr54; R129491.'


@pytest.fixture()
def f2_two_ccs():
    return 'AMERICAN FEDERAL TAX REPORTS. Vol. 5-6, no. 1, Feb. 1927. © West Pub. Co. (PWH)|v. 6, no. 1. © 23Feb27; A972256. 5Apr54; R128596'


@pytest.fixture()
def f2_pub_abroad():
    return 'AMUNDSEN, ROALD ENGELBREGT GRAVNING.|First crossing of the Polar Sea, by Roald Amundsen and Lincoln Ellsworth; with additional chapters by other members of the expedition. (Pub. abroad under title: The first flight across the Polar Sea) © 15Apr27; (pub. abroad 25Feb27, AI-9217); A972756. Mary-Louise Ellsworth (W); 19Apr54; R129296.'


@pytest.fixture()
def f2_on_matter():
    return 'ANDREWS, MARY RAYMOND SHIPMAN.|The perfect tribute; illustrated by Wilfred Jones. © on front. & decorations; 8Oct26; A950706. Charles Scribner\'s Sons (PWH); 24Jun54; R132516.'


@pytest.fixture()
def f2_date_reg_pairs():
    return 'BALMER, EDWIN.|Flying death. (In Liberty. May 8-June 12, 1926) © 8May26, B699781; 15May26, B700461; 22May26, B701226; 29May26, B701614; 5Jun26, B702507; 12Jun26, B703457. Edwin Balmer (A); 10Aug53; R126461-126466.'


@pytest.fixture()
def f2_three_parts():
    return 'BRAASCH, WILLIAM KARL.|Special supplementary bulletin. Nos. 1-7. © W. K. Braasch (A)|no. 2. © 24May26; A896875. 12May54; R130352.'


@pytest.fixture()
def f2_three_parts_pub_abroad():
    return 'PEDLER, MARGARET.|Yesterday\'s harvest. (Pub. abroad in installments in the Yellow magazine, July 9-Sept. 3, 1926. Illus. by M. MacMichael) © 28Dec26; A958935. Flora Mabel Warhurst & Harold Pincott (E); 4Jan54; R123834-R123837.|July 9. © 9Jul26; AI-8495.'


@pytest.fixture()
def f2_three_parts_on_matter():
    return 'MORLEY, CHRISTOPHER.|The Haverford edition of Christopher Morley. © Christopher Morley (A)|1. Parnassus on wheels. Kathleen. © on revisions; 29Jul27; A999443. 1Oct54; R136623.'


@pytest.fixture()
def f2_incomplete_reg_ids():
    return 'AMERICAN DIGEST.|Third decennial edition of the American digest, 1926. v.1-4. © 30Jan28, A1068234; 18Feb28, A1068235; 8Mar28, A1068880; 30Mar28, A1077175. West Pub. Co. (PWH); 4Apr55; R148105-148106, 148126, 148129.'


@pytest.fixture()
def f2_three_parts_post_claim():
    return 'COLLINS, DALE.|The sentimentalists. (In The Royal magazine, Dec. 1926-Mar. 1927) © Dale Collins (A) Chapter|19-24. © 22Nov26; AI-8848. 19Nov54; R148665.'


@pytest.fixture()
def f2_see_also_renewal():
    return 'BOYKIN, EDWARD C.|Everybody\'s look and play piano course, by Edward C. Boykin, pseud. of Osbourne McConathy. © 7Oct27; A1009237. Elizabeth Aikens & Osbourne Wm. McConathy (C); 23Sep55; R156196. (See also R143669)'


@pytest.fixture()
def f2_rearrange_regnum():
    return 'HUDSON, W. H.|Green mansions. Introd. by William Beebe; illus. by Edward A. Wilson. © 25Feb35; A85086. © on introd., illus. & design; George Macy Companies, Inc. (PWH); 25Feb63; R312848.'


@pytest.fixture()
def f3_simple():
    return 'R554644. War injuries of the extremities. By Paul W. Roder. © 20Jul45; AA488754. Ciba Geigy Corporation (PWH); 25Jun73; R554644.'


@pytest.fixture()
def f3_final_title_parens():
    return 'R594391. List of parts, machine number 300W201. Form 2936W (147) By The Singer Manufacturing Company. NM: new illus. & plates. © 20Feb47; AA46107. The Singer Company (PWH); 2Jan75; R594391.'


@pytest.fixture()
def f3_extra_title():
    return 'R566183. This bright dream. By Stephen Vincent Benet. (In The Last circle) © 18Nov46; A8670. Thomas C. Benet, Rachel Benet Lewis & Stephenie Benet Mahin (PPW); 20Dec73; R566183.'


@pytest.fixture()
def f3_new_matter():
    return 'R566276. New guide to recorded music. By Irving Kolodin. © on additions & revisions; 12Dec46; A9336. Irving Kolodin (A); 20Dec73; R566276.'


@pytest.fixture()
def f3_no_matter_no_author():
    return 'R594483. Advance California appellate reports. Vol.8, no.2. NM: headnotes, summaries, tables & index. © 10Jan47; AA45061. Bancroft-Whitney Company (PWH); 30Dec74; R594483.'


@pytest.fixture()
def not_parsed():
    return 'AMERICAN Federal tax reports. © West Pub. Co. (PWH) November, 1923. v. 1. © 28Dec23, A777088. R72760, 8Jan51.'


@pytest.fixture()
def f1_not_parsed_with_range():
    return 'ADVENTURE. © Popular publications, inc. (PCW) v. 43, nos. 1-6, Oct. 10-Nov. 30, 1923. © 4Sep23, B584848, 8Sep23, B585123; 20Sep23, B586126; 1Oct23, B586826; 8Oct23, B587442; 18Oct23, B588064. R69124-69129, 1Nov50.'


@pytest.fixture()
def f2_not_parsed():
    return 'HORN, ERNEST, comp. Most-used shorthand forms. © 14Nov27; A1013186. McGraw-Hill Book Co., Inc.; 4Feb55; R144252.'


@pytest.fixture()
def f2_not_parsed_with_range():
    return 'AMERICAN LAW REPORTS ANNOTATED. Vol. 65-71. Editors-in-chief: George H. Parmele and M. Blair Wailes. Consulting editor, William M. McKinney. Managing editors: Charles Porterfield and Edwin Stacey Oakes, assisted by the publishers\' editorial staff of the United States. © 6May30, A23371; 20Jun30, A25264; 22Aug30, A26833; 31Oct30, A29840; 8Dec30, A32190; 2Feb31, A34166; 13Apr31, A36786. Lawyers Cooperative Pub. Co. & Bancroft-Whitney Co. (PCW); 28Apr58; R213945, 213990, 213996, 214003, 214008, 214013, 214016.'

@pytest.fixture()
def f3_not_parsed():
    return 'R621591. Late have I loved thee. By Ethel Mannin. U.S. ed. pub. 30Sep48, A25796. © 29Jan48; AI-1804. Ethel Mannin (A); 8Dec75; R621591. (AI reg. entered under British Proclamation of 10Mar44)'


class TestShift(object):
    def test_shift_dates(self):
        s = '30Dec22, A695089. R59809, 17Mar50, Breitkopf Publications, inc., successor to Breitkopf & Haertel, inc. (PWH)'
        x =          'A695089. R59809, 17Mar50, Breitkopf Publications, inc., successor to Breitkopf & Haertel, inc. (PWH)'
        assert parse.shift_dates(s) == (x, ['1922-12-30'])
        assert parse.shift_dates('15Nov22, 15Dec22, B551759') == \
            ('B551759', ['1922-11-15', '1922-12-15'])
        assert parse.shift_dates('31Jun42; B552877.') == \
            ('B552877.', [None])


    def test_shift_regnums(self):
        assert parse.shift_regnums('A695089. R59809') == \
            ('R59809', ['A695089'])
        assert parse.shift_regnums('B551759, B567153. R56538-56539') == \
            ('R56538-56539', ['B551759', 'B567153'])


    def test_shift_rids(self):
        assert parse.shift_rids('R59809, 17Mar50, Breitkopf (PWH)') == \
            ('17Mar50, Breitkopf (PWH)', ['R59809'])

        assert parse.shift_rids('R61801, R61806, R61808, R61815, 28Apr50, The Lawyers Co-operative Publishing Co. (PCW)') == \
            ('28Apr50, The Lawyers Co-operative Publishing Co. (PCW)', 
             ['R61801', 'R61806', 'R61808', 'R61815'])

        assert parse.shift_rids('R148105-148107, 148126, 148129.') == \
            ('', ['R148105', 'R148106', 'R148107', 'R148126', 'R148129'])

        assert parse.shift_rids('R148129.') == \
            ('', ['R148129'])

        assert parse.shift_rids('R148129') == \
            ('', ['R148129'])

        assert parse.shift_rids('R123834-R123837.') == \
            ('', ['R123834', 'R123835', 'R123836', 'R123837'])

        with pytest.raises(TypeError):
            parse.shift_rids('(something else) R59809, 17Mar50, Breitkopf Publications, inc., successor to Breitkopf & Haertel, inc. (PWH)')
    
    
    def test_shift_pub_abroad(self):
        s = '(pub. abroad 15Feb23, AI-4905), A704583. R60233, 28Mar50, Elsie Bambridge (C)'
        assert parse.shift_pub_abroad(s) == \
            ('A704583. R60233, 28Mar50, Elsie Bambridge (C)',
             'pub. abroad|1923-02-15|AI-4905')


    def test_shift_see_also(self):
        assert parse.shift_see_also('(See also R147647)') == \
            ('', 'R147647', None)

        assert parse.shift_see_also(
            '(See also R147647, R147648, R148637, R148658-148664)') == \
            ('', 'R147647|R147648|R148637|R148658|R148659|R148660|R148661|R148662|R148663|R148664', None)

        assert parse.shift_see_also('(See also A1077787)') == \
            ('', None, 'A1077787')

        assert parse.shift_see_also('(See also AI-9939)') == \
            ('', None, 'AI-9939')


class TestTitleParsing(object):
    def test_simplest(self):
        t = 'ACTUAL BUSINESS ENGLISH, by P. H. Deffendall.'
        assert parse.get_author_title(t) == \
            ('P. H. Deffendall.', 'ACTUAL BUSINESS ENGLISH')


    def test_second_part(self):
        t = 'A. E. UHE, by Frederick H. Martens. (Little biographies: series 1, Musicians)'
        assert parse.get_author_title(t) == \
            ('Frederick H. Martens.', 'A. E. UHE (Little biographies: series 1, Musicians)')

    
    def test_with_pub_abroad(self):
        t = 'AND THE DEAD SPAKE; AND THE HORROR-HORN, by E. F. Benson. Pub. in England in Hutchinson\'s magazine, Sept.-Oct. 1922, under titles "The horror-horn" and "And the dead spake"; illustrated by "Blam."'
        assert parse.get_author_title(t) == \
            ('E. F. Benson.', 'AND THE DEAD SPAKE; AND THE HORROR-HORN Pub. in England in Hutchinson\'s magazine, Sept.-Oct. 1922, under titles "The horror-horn" and "And the dead spake"; illustrated by "Blam."')


    def test_bail_on_brackets(self):
        t = 'AND WITH HIS ROYAL SHAPE, by [International Feature Service, inc., as employer for hire of George] Herriman. (In Krazy Kat)'
        assert parse.get_author_title(t) == \
            (None, 'AND WITH HIS ROYAL SHAPE, by [International Feature Service, inc., as employer for hire of George] Herriman. (In Krazy Kat)')


    def test_numbered_eds(self):
        t = 'THE ART OF ANESTHESIA, by Paluel J. Flagg. 3d rev. ed.'
        assert parse.get_author_title(t) == \
            ('Paluel J. Flagg.', 'THE ART OF ANESTHESIA, 3d rev. ed.')

        t = 'THE BEAUTIFUL NECESSITY, seven essays on Theosophy and architecture, by Claude Bragdon. 2d ed.'
        assert parse.get_author_title(t) == \
            ('Claude Bragdon.', 'THE BEAUTIFUL NECESSITY, seven essays on Theosophy and architecture, 2d ed.')

        t = 'COMMERCIAL ATLAS OF AMERICA, by Rand, McNally and Company. 54th ed.'
        assert parse.get_author_title(t) == \
            ('Rand, McNally and Company.', 'COMMERCIAL ATLAS OF AMERICA, 54th ed.')

        t = 'DIETETICS FOR NURSES, by Fairfax T. Proudfit. 2d ed., rev.'
        assert parse.get_author_title(t) == \
            ('Fairfax T. Proudfit.', 'DIETETICS FOR NURSES, 2d ed., rev.')

        t = 'Guide to the study of the anatomy of the shark, necturus, and the cat. By Samuel Eddy & Clarence P. Oliver. 2nd ed.'
        assert parse.get_f3_author_title(t) == \
            ('Samuel Eddy & Clarence P. Oliver.', 'Guide to the study of the anatomy of the shark, necturus, and the cat., 2nd ed.')

        t = 'Preparing the research paper. By Robert H. Schmitz. 3rd ed.'
        assert parse.get_f3_author_title(t) == \
            ('Robert H. Schmitz.', 'Preparing the research paper., 3rd ed.')
        
    def test_bail_on_numbers_in_auth(self):
        t = 'ADDRESS, by Rudyard Kipling, at the annual dinner of the Royal College of Surgeons, Feb. 14, 1923. Pub. in England in the Morning post, Feb. 15, 1923, as The mystery of man\'s triumphs of surgery.'
        assert parse.get_author_title(t) == \
            (None, t)

        
        
class TestFormat1(object):
    def test_f1_simplest(self, simple):
        parsed = parse.parse('4', '1', simple)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'Frederick H. Martens.'
        assert parsed[0]['title'] == 'A. E. UHE (Little biographies: series 1, Musicians)'
        assert parsed[0]['odat'] == '1922-12-30'
        assert parsed[0]['oreg'] == 'A695089'
        assert parsed[0]['id'] == 'R59809'
        assert parsed[0]['rdat'] == '1950-03-17'
        assert parsed[0]['claimants'] == 'Breitkopf Publications, inc., successor to Breitkopf & Haertel, inc.|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['notes'] is None


    def test_f1_simple_auth_title(self, simple_auth_title):
        parsed = parse.parse('4', '1', simple_auth_title)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'P. H. Deffendall.'
        assert parsed[0]['title'] == 'ACTUAL BUSINESS ENGLISH'
        
        assert parsed[0]['odat'] == '1922-08-01'
        assert parsed[0]['oreg'] == 'A681161'
        assert parsed[0]['id'] == 'R60449'
        assert parsed[0]['rdat'] == '1950-04-05'
        assert parsed[0]['claimants'] == 'P. H. Deffendall|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['notes'] is None


    def test_numbered_edition(self, f1_numbered_edition):
        parsed = parse.parse('4', '1', f1_numbered_edition)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'Paluel J. Flagg.'
        assert parsed[0]['title'] == 'THE ART OF ANESTHESIA, 3d rev. ed.'
        
        assert parsed[0]['odat'] == '1922-10-18'
        assert parsed[0]['oreg'] == 'A692169'
        assert parsed[0]['id'] == 'R56339'
        assert parsed[0]['rdat'] == '1949-12-23'
        assert parsed[0]['claimants'] == 'Paluel J. Flagg|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['notes'] is None
        

    def test_f1_date_regnum_pairs(self, f1_reg_pairs):
        parsed = parse.parse('4', '1', f1_reg_pairs)
        assert len(parsed) == 4
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == "ABBOTT'S DIGEST OF ALL THE NEW YORK REPORTS. Apr., July, Oct., Dec. 1922."
        assert parsed[0]['odat'] == '1922-05-31'
        assert parsed[0]['oreg'] == 'B528574'
        assert parsed[0]['id'] == 'R61801'
        assert parsed[0]['rdat'] == '1950-04-28'
        assert parsed[0]['claimants'] == 'The Lawyers Co-operative Publishing Co.|PCW'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

        assert parsed[1]['odat'] == '1922-08-24'
        assert parsed[2]['odat'] == '1922-12-02'
        assert parsed[3]['odat'] == '1923-03-02'

        assert parsed[1]['oreg'] == 'B548911'
        assert parsed[2]['oreg'] == 'B553698'
        assert parsed[3]['oreg'] == 'B571736'
    
        assert parsed[1]['id'] == 'R61806'
        assert parsed[2]['id'] == 'R61808'
        assert parsed[3]['id'] == 'R61815'

        assert parsed[1]['rdat'] == '1950-04-28'
        assert parsed[2]['rdat'] == '1950-04-28'
        assert parsed[3]['rdat'] == '1950-04-28'


    def test_one_part_ren_mixed(self, one_part_ren_mixed):
        parsed = parse.parse('4', '1', one_part_ren_mixed)
        assert len(parsed) == 4
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'AMERICAN LAW REPORTS ANNOTATED. Cumulative index, v. 16-18, 16-19, 16-20, 22-23. Indexes to cases and notes combined.'
        assert parsed[0]['odat'] == '1922-07-13'
        assert parsed[0]['oreg'] == 'A683889'
        assert parsed[0]['id'] == 'R61784'
        assert parsed[0]['rdat'] == '1950-04-28'
        assert parsed[0]['claimants'] == 'The Lawyers Co-operative Publishing Co.|PCW||Bancroft-Whitney Co.|PCW'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

        assert parsed[1]['odat'] == '1922-09-06'
        assert parsed[1]['oreg'] == 'A683890'
        assert parsed[1]['id'] == 'R61785'
        assert parsed[1]['rdat'] == '1950-04-28'

        assert parsed[2]['odat'] == '1922-10-23'
        assert parsed[2]['oreg'] == 'A683891'
        assert parsed[2]['id'] == 'R61786'
        assert parsed[2]['rdat'] == '1950-04-28'

        assert parsed[3]['odat'] == '1923-04-23'
        assert parsed[3]['oreg'] == 'A704483'
        assert parsed[3]['id'] == 'R61796'
        assert parsed[3]['rdat'] == '1950-04-28'
    

    def test_single_interim(self, single_interim_pub):
        parsed = parse.parse('4', '1', single_interim_pub)
        assert len(parsed) == 1
        assert parsed[0]['author'] == None
        assert parsed[0]['title'] == 'ADDRESS, by Rudyard Kipling, at the annual dinner of the Royal College of Surgeons, Feb. 14, 1923. Pub. in England in the Morning post, Feb. 15, 1923, as The mystery of man\'s triumphs of surgery.'
        assert parsed[0]['odat'] == '1923-03-27'
        assert parsed[0]['oreg'] == 'A704583'
        assert parsed[0]['id'] == 'R60233'
        assert parsed[0]['rdat'] == '1950-03-28'
        assert parsed[0]['claimants'] == 'Elsie Bambridge|C'
        assert parsed[0]['previous'] == 'pub. abroad|1923-02-15|AI-4905'
        assert parsed[0]['new_matter'] is None


    def test_interim_pub_date_only(self, interim_pub_date_only):
        parsed = parse.parse('4', '1', interim_pub_date_only)
        assert len(parsed) == 1
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == "THE COOK'S WEDDING AND OTHER STORIES, from the Russian of Anton Chekhov. Constance Garnett, translator."
        assert parsed[0]['odat'] == '1922-03-21'
        assert parsed[0]['oreg'] == 'A659245'
        assert parsed[0]['id'] == 'R59404'
        assert parsed[0]['rdat'] == '1950-03-13'
        assert parsed[0]['claimants'] == 'David Garnett|C'
        assert parsed[0]['previous'] == 'pub. abroad|1922-02-02|'
        assert parsed[0]['new_matter'] is None

    
    def test_multiple_interim(self, multiple_interim_pub):
        parsed = parse.parse('4', '1', multiple_interim_pub)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'E. F. Benson.'
        assert parsed[0]['title'] == "AND THE DEAD SPAKE; AND THE HORROR-HORN Pub. in England in Hutchinson's magazine, Sept.-Oct. 1922, under titles \"The horror-horn\" and \"And the dead spake\"; illustrated by \"Blam.\""
        assert parsed[0]['odat'] == '1923-03-01'
        assert parsed[0]['oreg'] == 'A696722'
        assert parsed[0]['id'] == 'R59139'
        assert parsed[0]['rdat'] == '1950-03-03'
        assert parsed[0]['claimants'] == 'Kenneth Stewart Patrick McDowell|NK'
        assert parsed[0]['previous'] == 'pub. abroad|1922-08-24|AI-4680||pub. abroad|1922-09-16|AI-4725'
        assert parsed[0]['new_matter'] is None


    def test_simple_two_parts(self, simple_two_parts):
        parsed = parse.parse('4', '1', simple_two_parts)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'Arthur A. Noyes and Miles S. Sherrill. Complete ed.'
        assert parsed[0]['title'] == 'AN ADVANCED COURSE OF INSTRUCTION IN CHEMICAL PRINCIPLES'
        assert parsed[0]['odat'] == '1922-05-16'
        assert parsed[0]['oreg'] == 'A674144'
        assert parsed[0]['id'] == 'R59672'
        assert parsed[0]['rdat'] == '1950-03-20'
        assert parsed[0]['claimants'] == 'Clement Gould Noyes|NK'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_two_part_bracket_comment(self, two_part_bracket_comment):
        parsed = parse.parse('4', '1', two_part_bracket_comment)
        assert len(parsed) == 1
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'COL. WM. F. CODY, by Robert Lindneux. [Buffalo Bill, astride white horse; horse standing on brow of hill north-west of Cody, overlooking the town; Cedar and Rattlesnake mountains in background]'
        assert parsed[0]['odat'] == '1922-03-18'
        assert parsed[0]['oreg'] == 'G65236'
        assert parsed[0]['id'] == 'R59553'
        assert parsed[0]['rdat'] == '1950-03-09'
        assert parsed[0]['claimants'] == 'Robert Lindneux|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_two_preceding_info(self, two_part_preceding_info):
        parsed = parse.parse('4', '1', two_part_preceding_info)
        assert len(parsed) == 1
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'LES THIBAULT, par Roger Martin du Gard. t. 1: Le cahier gris.'
        assert parsed[0]['odat'] == '1922-05-01'
        assert parsed[0]['oreg'] == 'AF19918'
        assert parsed[0]['id'] == 'R61349'
        assert parsed[0]['rdat'] == '1950-04-24'
        assert parsed[0]['claimants'] == 'Roger Martin du Gard|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_renewal_id_range(self, renewal_id_range):
        parsed = parse.parse('4', '1', renewal_id_range)
        assert len(parsed) == 8
        assert parsed[0]['author'] == 'Hugh Lofting.'
        assert parsed[0]['title'] == 'ADVENTURES OF DOCTOR DOLITTLE (In the New York tribune, Dec. 24-31, 1922)'
        assert parsed[0]['odat'] == '1922-12-24'
        assert parsed[0]['oreg'] == 'B542207'
        assert parsed[0]['id'] == 'R63718'
        assert parsed[0]['rdat'] == '1950-06-23'
        assert parsed[0]['claimants'] == 'Josephine Lofting|W'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

        assert parsed[1]['odat'] == '1922-12-25'
        assert parsed[2]['odat'] == '1922-12-26'
        assert parsed[3]['odat'] == '1922-12-27'
        assert parsed[4]['odat'] == '1922-12-28'
        assert parsed[5]['odat'] == '1922-12-29'
        assert parsed[6]['odat'] == '1922-12-30'
        assert parsed[7]['odat'] == '1922-12-31'

        assert parsed[1]['oreg'] == 'B542208'
        assert parsed[2]['oreg'] == 'B542209'
        assert parsed[3]['oreg'] == 'B542210'
        assert parsed[4]['oreg'] == 'B542211'
        assert parsed[5]['oreg'] == 'B542212'
        assert parsed[6]['oreg'] == 'B542213'
        assert parsed[7]['oreg'] == 'B542214'
    
        assert parsed[1]['id'] == 'R63719'
        assert parsed[2]['id'] == 'R63720'
        assert parsed[3]['id'] == 'R63721'
        assert parsed[4]['id'] == 'R63722'
        assert parsed[5]['id'] == 'R63723'
        assert parsed[6]['id'] == 'R63724'
        assert parsed[7]['id'] == 'R63725'

        assert parsed[1]['rdat'] == '1950-06-23'
        assert parsed[2]['rdat'] == '1950-06-23'
        assert parsed[3]['rdat'] == '1950-06-23'
        assert parsed[4]['rdat'] == '1950-06-23'
        assert parsed[5]['rdat'] == '1950-06-23'
        assert parsed[6]['rdat'] == '1950-06-23'
        assert parsed[7]['rdat'] == '1950-06-23'


    def test_chiastic_id_range(self, chiastic_id_range):
        parsed = parse.parse('4', '1', chiastic_id_range)
        assert len(parsed) == 2
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == "AINSLEE'S. v. 50, nos. 4-5, Dec. 1922-Jan. 1923."
        assert parsed[0]['odat'] == '1922-11-15'
        assert parsed[0]['oreg'] == 'B551759'
        assert parsed[0]['id'] == 'R56538'
        assert parsed[0]['rdat'] == '1949-12-30'
        assert parsed[0]['claimants'] == 'Street & Smith Publications, inc.|PCW'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

        assert parsed[1]['odat'] == '1922-12-15'
        assert parsed[1]['oreg'] == 'B567153'
        assert parsed[1]['id'] == 'R56539'
        assert parsed[1]['rdat'] == '1949-12-30'


    def test_many_reg_dates_one_reg_num(self, many_reg_dates_one_reg_num):
        parsed = parse.parse('4', '1', many_reg_dates_one_reg_num)
        assert len(parsed) == 4
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == "CATHERINE, comédie en 4. actes de Henri Lavedan. (In Les Annales, nos. 2061-2064)"
        assert parsed[0]['odat'] == '1922-12-24'
        assert parsed[0]['oreg'] == 'D63725'
        assert parsed[0]['id'] == 'R61029'
        assert parsed[0]['rdat'] == '1950-04-17'
        assert parsed[0]['claimants'] == 'Mme veuve Henri Lavedan, née Pauline Auguez|W'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

        assert parsed[1]['odat'] == '1922-12-31'
        assert parsed[2]['odat'] == '1923-01-07'
        assert parsed[3]['odat'] == '1923-01-14'
    
        assert parsed[1]['oreg'] == 'D63725'
        assert parsed[2]['oreg'] == 'D63725'
        assert parsed[3]['oreg'] == 'D63725'

        assert parsed[1]['id'] == 'R61029'
        assert parsed[2]['id'] == 'R61029'
        assert parsed[3]['id'] == 'R61029'

        assert parsed[1]['rdat'] == '1950-04-17'
        assert parsed[2]['rdat'] == '1950-04-17'
        assert parsed[3]['rdat'] == '1950-04-17'


    def test_one_date_list_of_regnums(self, one_date_list_of_regnums):
        parsed = parse.parse('4', '1', one_date_list_of_regnums)
        assert len(parsed) == 2
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'SOUTH CAROLINA DIGEST, 1783-1886. v. 1-2.'
        assert parsed[0]['odat'] == '1922-12-02'
        assert parsed[0]['oreg'] == 'A698474'
        assert parsed[0]['id'] == 'R57358'
        assert parsed[0]['rdat'] == '1950-01-16'
        assert parsed[0]['claimants'] == 'West Publishing Co.|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        
        assert parsed[1]['odat'] == '1922-12-02'
        assert parsed[1]['oreg'] == 'A698473'
        assert parsed[1]['id'] == 'R57359'
        assert parsed[1]['rdat'] == '1950-01-16'

    @pytest.mark.xfail
    def test_date_range_one_regnum(self, date_range_one_regnum):
        parsed = parse.parse('4', '1', date_range_one_regnum)
        assert len(parsed) == 1
        assert parsed[0]['title'] == 'REINE DE TANGO, grand roman, inédit par Marcel Priollet. 24 installments. (In Echo du nord, Lille)'
        assert parsed[0]['odat'] == '1922-11-10'
        assert parsed[0]['oreg'] == 'AF22373'
        assert parsed[0]['id'] == 'R61026'
        assert parsed[0]['rdat'] == '1950-04-14'
        assert parsed[0]['claimants'] == 'Marcel Priollet|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['notes'] == 'This entry has multiple copyright dates not listed here under one copyright registration number'
    
    
    def test_new_matter(self, new_matter):
        parsed = parse.parse('4', '1', new_matter)
        assert len(parsed) == 1
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'AMERICAN POCKET MEDICAL DICTIONARY; W. A. Newman Dorland, editor. 12th ed., rev.'
        assert parsed[0]['odat'] == '1922-05-22'
        assert parsed[0]['oreg'] == 'A661865'
        assert parsed[0]['id'] == 'R59332'
        assert parsed[0]['rdat'] == '1950-03-07'
        assert parsed[0]['claimants'] == 'W. B. Saunders Co.|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] == 'new matter'


    def test_on_illus(self, class_code_phrase):    
        parsed = parse.parse('4', '1', class_code_phrase)
        assert parsed[0]['new_matter'] == 'illus.'
    

    def test_class_code_phrase(self, class_code_phrase):
        parsed = parse.parse('4', '1', class_code_phrase)
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'THE FAIRY BOOK, by Dinah Maria Mulock [Craik] Illus. by Louis Rhead.'
        assert parsed[0]['claimants'] == 'Stephen Yates|NK of Louis Rhead'


    @pytest.mark.xfail
    def test_missing_class_code(self, missing_class_code):
        parsed = parse.parse('4', '1', missing_class_code)
        assert len(parsed) == 1
        assert parsed[0]['title'] == "FRANKLIN'S HOMECOMING, High Street wharf, Philadelphia, by Jean Leon Gerome Ferris. [Group picture, ship at center]"
        assert parsed[0]['odat'] == '1923-03-28'
        assert parsed[0]['oreg'] == 'G68152'
        assert parsed[0]['id'] == 'R63588'
        assert parsed[0]['rdat'] == '1950-06-23'
        assert parsed[0]['claimants'] == 'Ernest N. Ryder, administrator d.b.n.c.t.a. estate of author.|'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_ny_herald(self, ny_herald):
        parsed = parse.parse('4', '1', ny_herald)
        assert len(parsed) == 31
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'NEW YORK HERALD. v. 86, no. 336-v. 87, no. 1, Aug. 1-31, 1922.'
        assert parsed[0]['odat'] == '1922-08-01'
        assert parsed[0]['oreg'] == 'B541697'
        assert parsed[0]['id'] == 'R65000'
        assert parsed[0]['rdat'] == '1950-07-28'
        assert parsed[0]['claimants'] == 'New York Herald Tribune, inc.|PCW'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

        assert parsed[30]['odat'] == '1922-08-31'
        assert parsed[30]['oreg'] == 'B541727'
        assert parsed[30]['id'] == 'R65030'
        assert parsed[30]['rdat'] == '1950-07-28'


    @pytest.mark.xfail
    def test_pub_abroad_at_end(self, pub_abroad_at_end):
        parsed = parse.parse('4', '1', pub_abroad_at_end)
        assert len(parsed) == 1
        assert parsed[0]['title'] == "FRANKLIN'S HOMECOMING, High Street wharf, Philadelphia, by Jean Leon Gerome Ferris. [Group picture, ship at center]"
        assert parsed[0]['odat'] == '1923-03-28'
        assert parsed[0]['oreg'] == 'G68152'
        assert parsed[0]['id'] == 'R63588'
        assert parsed[0]['rdat'] == '1950-06-23'
        assert parsed[0]['claimants'] == 'Ernest N. Ryder, administrator d.b.n.c.t.a. estate of author.|'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

    @pytest.mark.xfail
    def test_patent_office(patent_office):
        parsed = parse.parse('4', '1', patent_office)
        assert len(parsed) == 1


    def test_label_id(self, label_id):
        parsed = parse.parse('4', '1', label_id)
        assert len(parsed) == 1
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'BEN-GAY. (Medicinal preparation for rheumatism, gout and neuralgia)'
        assert parsed[0]['oreg'] == 'Label 24762'


    def test_chiastic_three_part(self, chiastic_three_part):
        parsed = parse.parse('4', '1', chiastic_three_part)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'Arthur C. Train.'
        assert parsed[0]['title'] == 'DESERT RUBAIYAT (In McCall\'s magazine) June 1923 issue.'
        assert parsed[0]['odat'] == '1923-05-10'
        assert parsed[0]['oreg'] == 'B576564'
        assert parsed[0]['id'] == 'R69499'
        assert parsed[0]['rdat'] == '1950-11-08'
        assert parsed[0]['claimants'] == 'Helen C. Train|W'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_only_numbers(self, not_parsed):
        parsed = parse.parse('5', '1', not_parsed)
        assert len(parsed) == 1
        assert parsed[0]['odat'] == '1923-12-28'
        assert parsed[0]['oreg'] == 'A777088'
        assert parsed[0]['id'] == 'R72760'
        assert parsed[0]['rdat'] == '1951-01-08'
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] is None
        assert parsed[0]['claimants'] is None
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None
        
        
    def test_only_numbers_with_range(self, f1_not_parsed_with_range):
        parsed = parse.parse('4', '1', f1_not_parsed_with_range)
        assert len(parsed) == 6
        assert parsed[0]['odat'] == '1923-09-04'
        assert parsed[0]['oreg'] == 'B584848'
        assert parsed[0]['id'] == 'R69124'
        assert parsed[0]['rdat'] == '1950-11-01'
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] is None
        assert parsed[0]['claimants'] is None
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None

        assert parsed[5]['odat'] == '1923-10-18'
        assert parsed[5]['oreg'] == 'B588064'
        assert parsed[5]['id'] == 'R69129'
        assert parsed[5]['rdat'] == '1950-11-01'
        assert parsed[5]['author'] is None
        assert parsed[5]['title'] is None
        assert parsed[5]['claimants'] is None
        assert parsed[5]['previous'] is None
        assert parsed[5]['new_matter'] is None
        assert parsed[5]['see_also_ren'] is None 
        assert parsed[5]['see_also_reg'] is None
        

class TestFormat2(object):
    def test_simplest(self, f2_simplest):
        parsed = parse.parse('8', '1', f2_simplest)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'ABBOTT, AUSTIN.'
        assert parsed[0]['title'] == 'Digest of all the New York reports, 1925.'
        assert parsed[0]['odat'] == '1926-08-14'
        assert parsed[0]['oreg'] == 'A901544'
        assert parsed[0]['id'] == 'R129491'
        assert parsed[0]['rdat'] == '1954-04-21'
        assert parsed[0]['claimants'] == 'Lawyers Co-operative Pub. Co.|PCW'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_two_ccs(self, f2_two_ccs):
        parsed = parse.parse('8', '1', f2_two_ccs)
        assert len(parsed) == 1
        assert parsed[0]['title'] == 'AMERICAN FEDERAL TAX REPORTS. Vol. 5-6, no. 1, Feb. 1927. v. 6, no. 1.'
        assert parsed[0]['odat'] == '1927-02-23'
        assert parsed[0]['oreg'] == 'A972256'
        assert parsed[0]['id'] == 'R128596'
        assert parsed[0]['rdat'] == '1954-04-05'
        assert parsed[0]['claimants'] == 'West Pub. Co.|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        

    def test_f2_pub_abroad(self, f2_pub_abroad):
        parsed = parse.parse('8', '1', f2_pub_abroad)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'AMUNDSEN, ROALD ENGELBREGT GRAVNING.'
        assert parsed[0]['title'] == 'First crossing of the Polar Sea, by Roald Amundsen and Lincoln Ellsworth; with additional chapters by other members of the expedition. (Pub. abroad under title: The first flight across the Polar Sea)'
        assert parsed[0]['odat'] == '1927-04-15'
        assert parsed[0]['oreg'] == 'A972756'
        assert parsed[0]['id'] == 'R129296'
        assert parsed[0]['rdat'] == '1954-04-19'
        assert parsed[0]['claimants'] == 'Mary-Louise Ellsworth|W'
        assert parsed[0]['previous'] == 'pub. abroad|1927-02-25|AI-9217'
        assert parsed[0]['new_matter'] is None

    def test_f2_on_matter(self, f2_on_matter):
        parsed = parse.parse('8', '1', f2_on_matter)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'ANDREWS, MARY RAYMOND SHIPMAN.'
        assert parsed[0]['title'] == 'The perfect tribute; illustrated by Wilfred Jones.'
        assert parsed[0]['odat'] == '1926-10-08'
        assert parsed[0]['oreg'] == 'A950706'
        assert parsed[0]['id'] == 'R132516'
        assert parsed[0]['rdat'] == '1954-06-24'
        assert parsed[0]['claimants'] == 'Charles Scribner\'s Sons|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] == 'front. & decorations'


    def test_date_reg_pairs(self, f2_date_reg_pairs):
        parsed = parse.parse('8', '1', f2_date_reg_pairs)
        assert len(parsed) == 6
        assert parsed[0]['author'] == 'BALMER, EDWIN.'
        assert parsed[0]['title'] == 'Flying death. (In Liberty. May 8-June 12, 1926)'
        assert parsed[0]['odat'] == '1926-05-08'
        assert parsed[0]['oreg'] == 'B699781'
        assert parsed[0]['id'] == 'R126461'
        assert parsed[0]['rdat'] == '1953-08-10'
        assert parsed[0]['claimants'] == 'Edwin Balmer|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_three_parts(self, f2_three_parts):
        parsed = parse.parse('8', '1', f2_three_parts)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'BRAASCH, WILLIAM KARL.'
        assert parsed[0]['title'] == 'Special supplementary bulletin. Nos. 1-7. no. 2.'
        assert parsed[0]['odat'] == '1926-05-24'
        assert parsed[0]['oreg'] == 'A896875'
        assert parsed[0]['id'] == 'R130352'
        assert parsed[0]['rdat'] == '1954-05-12'
        assert parsed[0]['claimants'] == 'W. K. Braasch|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    @pytest.mark.xfail
    def test_three_parts_pub_abroad(self, f2_three_parts_pub_abroad):
        parsed = parse.parse('8', '1', f2_three_parts_pub_abroad)
        assert len(parsed) == 4
        assert parsed[0]['author'] == 'PEDLER, MARGARET.'
        assert parsed[0]['title'] == 'Yesterday\'s harvest. (Pub. abroad in installments in the Yellow magazine, July 9-Sept. 3, 1926. Illus. by M. MacMichael)'
        assert parsed[0]['odat'] == '1926-12-28'
        assert parsed[0]['oreg'] == 'A958935'
        assert parsed[0]['id'] == 'R123834'
        assert parsed[0]['rdat'] == '1954-01-04'
        assert parsed[0]['claimants'] == 'Flora Mabel Warhurst & Harold Pincott|E'
        assert parsed[0]['previous'] is '|9Jul26|AI-8495'
        assert parsed[0]['new_matter'] is None


    def test_three_parts_on_matter(self, f2_three_parts_on_matter):
        parsed = parse.parse('8', '1', f2_three_parts_on_matter)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'MORLEY, CHRISTOPHER.'
        assert parsed[0]['title'] == 'The Haverford edition of Christopher Morley. 1. Parnassus on wheels. Kathleen.'
        assert parsed[0]['odat'] == '1927-07-29'
        assert parsed[0]['oreg'] == 'A999443'
        assert parsed[0]['id'] == 'R136623'
        assert parsed[0]['rdat'] == '1954-10-01'
        assert parsed[0]['claimants'] == 'Christopher Morley|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] == 'revisions'


    def test_temp(self, f2_incomplete_reg_ids):
        parsed = parse.parse('9', '1', f2_incomplete_reg_ids)
        assert len(parsed) == 4
        assert parsed[0]['author'] == 'AMERICAN DIGEST.'
        assert parsed[0]['title'] == 'Third decennial edition of the American digest, 1926. v.1-4.'
        assert parsed[0]['odat'] == '1928-01-30'
        assert parsed[0]['oreg'] == 'A1068234'
        assert parsed[0]['id'] == 'R148105'
        assert parsed[0]['rdat'] == '1955-04-04'
        assert parsed[0]['claimants'] == 'West Pub. Co.|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None

        assert parsed[3]['odat'] == '1928-03-30'
        assert parsed[3]['oreg'] == 'A1077175'
        assert parsed[3]['id'] == 'R148129'
        assert parsed[3]['rdat'] == '1955-04-04'
        

    def test_three_part_two_cc(self, format_two_two_cc):
        parsed = parse.parse('8', '1', format_two_two_cc)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'ABBOTT, AUSTIN.'
        assert parsed[0]['title'] == 'Digest of all the New York reports. Third supplement, 1918-1924. Vol. 4-5. v. 4.'
        assert parsed[0]['odat'] == '1926-05-03'
        assert parsed[0]['oreg'] == 'A890950'
        assert parsed[0]['id'] == 'R129485'
        assert parsed[0]['rdat'] == '1954-04-21'
        assert parsed[0]['claimants'] == 'Lawyers Co-operative Pub. Co.|PCW'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_three_parts_post_claim(self, f2_three_parts_post_claim):
        parsed = parse.parse('9', '1', f2_three_parts_post_claim)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'COLLINS, DALE.'
        assert parsed[0]['title'] == 'The sentimentalists. (In The Royal magazine, Dec. 1926-Mar. 1927) Chapter 19-24.'
        assert parsed[0]['odat'] == '1926-11-22'
        assert parsed[0]['oreg'] == 'AI8848'
        assert parsed[0]['id'] == 'R148665'
        assert parsed[0]['rdat'] == '1954-11-19'
        assert parsed[0]['claimants'] == 'Dale Collins|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None


    def test_f2_see_also_renewal(self, f2_see_also_renewal):
        parsed = parse.parse('9', '1', f2_see_also_renewal)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'BOYKIN, EDWARD C.'
        assert parsed[0]['title'] == 'Everybody\'s look and play piano course, by Edward C. Boykin, pseud. of Osbourne McConathy.'
        assert parsed[0]['odat'] == '1927-10-07'
        assert parsed[0]['oreg'] == 'A1009237'
        assert parsed[0]['id'] == 'R156196'
        assert parsed[0]['rdat'] == '1955-09-23'
        assert parsed[0]['claimants'] == 'Elizabeth Aikens & Osbourne Wm. McConathy|C'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] == 'R143669'
        assert parsed[0]['see_also_reg'] == None


    def test_rearrange_regnum(self, f2_rearrange_regnum):
        parsed = parse.parse('17', '1', f2_rearrange_regnum)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'HUDSON, W. H.'
        assert parsed[0]['title'] == 'Green mansions. Introd. by William Beebe; illus. by Edward A. Wilson.'
        assert parsed[0]['odat'] == '1935-02-25'
        assert parsed[0]['oreg'] == 'A85086'
        assert parsed[0]['id'] == 'R312848'
        assert parsed[0]['rdat'] == '1963-02-25'
        assert parsed[0]['claimants'] == 'George Macy Companies, Inc.|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] == 'introd., illus. & design'
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


    def test_only_numbers(self, f2_not_parsed):
        parsed = parse.parse('9', '1', f2_not_parsed)
        assert len(parsed) == 1
        assert parsed[0]['odat'] == '1927-11-14'
        assert parsed[0]['oreg'] == 'A1013186'
        assert parsed[0]['id'] == 'R144252'
        assert parsed[0]['rdat'] == '1955-02-04'
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] is None
        assert parsed[0]['claimants'] is None
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


    def test_only_numbers_with_range(self, f2_not_parsed_with_range):
        parsed = parse.parse('9', '1', f2_not_parsed_with_range)
        assert len(parsed) == 7
        assert parsed[0]['odat'] == '1930-05-06'
        assert parsed[0]['oreg'] == 'A23371'
        assert parsed[0]['id'] == 'R213945'
        assert parsed[0]['rdat'] == '1958-04-28'
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] is None
        assert parsed[0]['claimants'] is None
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None

        assert parsed[6]['odat'] == '1931-04-13'
        assert parsed[6]['oreg'] == 'A36786'
        assert parsed[6]['id'] == 'R214016'
        assert parsed[6]['rdat'] == '1958-04-28'
        assert parsed[6]['author'] is None
        assert parsed[6]['title'] is None
        assert parsed[6]['claimants'] is None
        assert parsed[6]['previous'] is None
        assert parsed[6]['new_matter'] is None
        assert parsed[6]['see_also_ren'] is None 
        assert parsed[6]['see_also_reg'] is None
        

    @pytest.mark.xfail
    def test_regnum_ranges(self, f2_regnum_ranges):
        parsed = parse.parse('12', '1', f2_regnum_ranges)
        assert len(parsed) == 7
        assert parsed[0]['author'] == 'WILLIAM J.'
        assert parsed[0]['title'] == 'Federal practice, jurisdiction & procedure, civil and criminal, with forms. Assisted by George C. Thorpe. Vol.5-11.'
        assert parsed[0]['odat'] == '1931-02-02'
        assert parsed[0]['oreg'] == 'A35829'
        assert parsed[0]['id'] == 'R214419'
        assert parsed[0]['rdat'] == '7May58'
        assert parsed[0]['claimants'] == 'William J. Hughes, Jr.|C'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None
        
        
class TestFormat3(object):
    def test_simplest(self, f3_simple):
        parsed = parse.parse('27', '2', f3_simple)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'Paul W. Roder.'
        assert parsed[0]['title'] == 'War injuries of the extremities.'
        assert parsed[0]['odat'] == '1945-07-20'
        assert parsed[0]['oreg'] == 'AA488754'
        assert parsed[0]['id'] == 'R554644'
        assert parsed[0]['rdat'] == '1973-06-25'
        assert parsed[0]['claimants'] == 'Ciba Geigy Corporation|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


    def test_final_parens(self, f3_final_title_parens):
        parsed = parse.parse('29', '1', f3_final_title_parens)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'The Singer Manufacturing Company.'
        assert parsed[0]['title'] == 'List of parts, machine number 300W201. Form 2936W (147)'
        assert parsed[0]['odat'] == '1947-02-20'
        assert parsed[0]['oreg'] == 'AA46107'
        assert parsed[0]['id'] == 'R594391'
        assert parsed[0]['rdat'] == '1975-01-02'
        assert parsed[0]['claimants'] == 'The Singer Company|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] == 'new illus. & plates.'
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


    def test_extra_title(self, f3_extra_title):
        parsed = parse.parse('28', '1', f3_extra_title)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'Stephen Vincent Benet.'
        assert parsed[0]['title'] == 'This bright dream. (In The Last circle)'
        assert parsed[0]['odat'] == '1946-11-18'
        assert parsed[0]['oreg'] == 'A8670'
        assert parsed[0]['id'] == 'R566183'
        assert parsed[0]['rdat'] == '1973-12-20'
        assert parsed[0]['claimants'] == 'Thomas C. Benet, Rachel Benet Lewis & Stephenie Benet Mahin|PPW'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


    def test_new_matter(self, f3_new_matter):
        parsed = parse.parse('28', '1', f3_new_matter)
        assert len(parsed) == 1
        assert parsed[0]['author'] == 'Irving Kolodin.'
        assert parsed[0]['title'] == 'New guide to recorded music.'
        assert parsed[0]['odat'] == '1946-12-12'
        assert parsed[0]['oreg'] == 'A9336'
        assert parsed[0]['id'] == 'R566276'
        assert parsed[0]['rdat'] == '1973-12-20'
        assert parsed[0]['claimants'] == 'Irving Kolodin|A'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] == 'additions & revisions'
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


    def test_new_matter_no_author(self, f3_no_matter_no_author):
        parsed = parse.parse('28', '1', f3_no_matter_no_author)
        assert len(parsed) == 1
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] == 'Advance California appellate reports. Vol.8, no.2.'
        assert parsed[0]['odat'] == '1947-01-10'
        assert parsed[0]['oreg'] == 'AA45061'
        assert parsed[0]['id'] == 'R594483'
        assert parsed[0]['rdat'] == '1974-12-30'
        assert parsed[0]['claimants'] == 'Bancroft-Whitney Company|PWH'
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] == 'headnotes, summaries, tables & index.'
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


    def test_only_numbers(self, f3_not_parsed):
        parsed = parse.parse('30', '1', f3_not_parsed)
        assert len(parsed) == 1
        assert parsed[0]['odat'] == '1948-01-29'
        assert parsed[0]['oreg'] == 'AI1804'
        assert parsed[0]['id'] == 'R621591'
        assert parsed[0]['rdat'] == '1975-12-08'
        assert parsed[0]['author'] is None
        assert parsed[0]['title'] is None
        assert parsed[0]['claimants'] is None
        assert parsed[0]['previous'] is None
        assert parsed[0]['new_matter'] is None
        assert parsed[0]['see_also_ren'] is None 
        assert parsed[0]['see_also_reg'] is None


def test_f2_simplest(format_two):
    parsed = parse.parse('26', format_two)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'A.L.R. CUMULATIVE INDEX-DIGEST. Vol.5, covering v.126-150.'
    assert parsed[0]['odat'] == '5Oct44'
    assert parsed[0]['oreg'] == 'A183343'
    assert parsed[0]['id'] == 'R525069'
    assert parsed[0]['rdat'] == '16Mar72'
    assert parsed[0]['claimants'] == 'Lawyers Co-operative Pub. Co. & Bancroft-Whitney Co.|PWH'
    assert parsed[0]['previous'] is None
    assert parsed[0]['new_matter'] is None


def test_two_part_format_two(two_part_format_two):
    parsed = parse.parse2(two_part_format_two)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'ABBETT, ROBERT W. Engineering contracts and specifications.'
    assert parsed[0]['odat'] == '8Jan45'
    assert parsed[0]['oreg'] == 'A185390'
    assert parsed[0]['id'] == 'R523485'
    assert parsed[0]['rdat'] == '17Jan72'
    assert parsed[0]['claimants'] == 'Robert W. Abbett|A'
    assert parsed[0]['previous'] is None
    assert parsed[0]['new_matter'] is None


def test_format_two_3_part_cc_one_three(format_two_3_part_cc_one_three):
    parsed = parse.parse2(format_two_3_part_cc_one_three)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'THE NEW YORK TIMES INDEX. Joseph C. Gephart, editor. v.32, no. 6.'
    assert parsed[0]['odat'] == '21Aug44'
    assert parsed[0]['oreg'] == 'AA463212'
    assert parsed[0]['id'] == 'R522151'
    assert parsed[0]['rdat'] == '26Jan72'
    assert parsed[0]['claimants'] == 'New York Times Co.|PWH'
    assert parsed[0]['previous'] is None
    assert parsed[0]['new_matter'] is None


def test_format_two_2_part_2_cc(format_two_2_part_2_cc):
    parsed = parse.parse2(format_two_2_part_2_cc)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'AMERICAN LAW REPORTS, ANNOTATED. Vol. 148.'
    assert parsed[0]['odat'] == '20Mar44'
    assert parsed[0]['oreg'] == 'A179593'
    assert parsed[0]['id'] == 'R524719'
    assert parsed[0]['rdat'] == '6Mar72'
    assert parsed[0]['claimants'] == 'Lawyers Co-operative Pub. Co. & Bancroft-Whitney Co.|PWH'
    assert parsed[0]['previous'] is None
    assert parsed[0]['new_matter'] is None


def test_f2_four_parts(f2_four_parts):
    parsed = parse.parse2(f2_four_parts)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'CALIFORNIA. DISTRICT COURTS OF APPEAL. Advance California appellate reports. J. O. Tucker, editor. v. 5, no. 27.'
    assert parsed[0]['odat'] == '14Jul44'
    assert parsed[0]['oreg'] == 'AA462954'
    assert parsed[0]['id'] == 'R530779'
    assert parsed[0]['rdat'] == '14Jun72'
    assert parsed[0]['claimants'] == 'Bancroft-Whitney Co.|PWH'
    assert parsed[0]['previous'] is None
    assert parsed[0]['new_matter'] is None


def test_f2_multiple_renewals(f2_multiple_renewals):
    parsed = parse.parse2(f2_multiple_renewals)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'CALIFORNIA. DISTRICT COURTS OF APPEAL. Advance California appellate reports. J. O. Tucker, editor. v. 5, no. 27.'
    assert parsed[0]['odat'] == '14Jul44'
    assert parsed[0]['oreg'] == 'AA462954'
    assert parsed[0]['id'] == 'R530779'
    assert parsed[0]['rdat'] == '14Jun72'
    assert parsed[0]['claimants'] == 'Bancroft-Whitney Co.|PWH'
    assert parsed[0]['previous'] is None
    assert parsed[0]['new_matter'] is None


def test_f2_on_translation(f2_on_translation):
    parsed = parse.parse2(f2_on_translation)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'CIANO, GALEAZZO, CONTE. The Ciano diaries, by Count Galeazzo. (In Chicago daily news) Appl. author: Countess Edda Ciano, employer for hire.  '
    assert parsed[0]['odat'] == '18Jun45'
    assert parsed[0]['oreg'] == 'B673449'
    assert parsed[0]['id'] == 'R537443'
    assert parsed[0]['rdat'] == '22Sep72'
    assert parsed[0]['claimants'] == 'Countess Edda Mussolini Ciano|PWH'
    assert parsed[0]['previous'] is None
    assert parsed[0]['new_matter'] == 'on translation'


def test_regnum_af(regnum_af):
    parsed = parse.parse(regnum_af)
    assert len(parsed) == 1
    assert parsed[0]['book'] == "LE COEUR CAMBRIOLÉ, une histoire éponvantable, la Hache d'or, par Gaston Leroux."
    assert parsed[0]['oreg'] == 'AF21459'


def test_regnum_aa(regnum_aa):
    parsed = parse.parse(regnum_aa)
    assert len(parsed) == 1
    assert parsed[0]['book'] == "LE CÔTÉ DE GUERMANTES [et] SODOME ET GOMORRHE II, par Marcel Proust. (His A la recherche du temps perdu, 2-3, t. 5) 3 v."
    assert parsed[0]['oreg'] == 'AA19985'


def test_regnum_a5(regnum_a5):
    parsed = parse.parse2(regnum_a5)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'ADAMSON, HAROLD. Bring on the girls. Words by Harold Adamson.'
    assert parsed[0]['oreg'] == 'A5-135834'


def test_regnum_ai(regnum_ai):
    parsed = parse.parse('8', regnum_ai)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'CROMPTON, RICHMAL. The house.'
    assert parsed[0]['oreg'] == 'AI-8054'

def test_regnum_b5(regnum_b5):
    parsed = parse.parse(regnum_b5)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'THE NEWLYWEDS, by Charles McManus. (In the New York journal, May 14, 1923)'
    assert parsed[0]['oreg'] == 'B5-14369'


def test_regnum_c(regnum_c):
    parsed = parse.parse(regnum_c)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'THE AUCTIONEER OFFERING A BARREL OF FUN, a monologue by George Heather.'
    assert parsed[0]['oreg'] == 'C2352'


def test_regnum_dp(regnum_dp):
    parsed = parse.parse(regnum_dp)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'ANNA KARENINA, Oper In 3 Aufzügen (vier Bildern) von Alexandar Goth, Deutsch von Hans Liebstoeckl. Musik von Jeno Hubay, Op.112. klavierauszug von A. Szikla.'
    assert parsed[0]['oreg'] == 'DP220'


def test_regnum_f(regnum_f):
    parsed = parse.parse(regnum_f)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'ATLAS OF HUMBOLDT COUNTY, CALIFORNIA, by Belcher Abstract and Title Company. Sheet no. 9.'
    assert parsed[0]['oreg'] == 'F37697'


def test_regnum_g(missing_class_code):
    parsed = parse.parse(missing_class_code)
    assert len(parsed) == 1
    assert parsed[0]['book'] == "FRANKLIN'S HOMECOMING, High Street wharf, Philadelphia, by Jean Leon Gerome Ferris. [Group picture, ship at center]"
    assert parsed[0]['oreg'] == 'G68152'


def test_regnum_i(regnum_i):
    parsed = parse.parse(regnum_i)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'DENTAL CHART SHOWING DRAWING OF TEETH, by Harry M. Chandler.'
    assert parsed[0]['oreg'] == 'I6581'


def test_regnum_iu(regnum_iu):
    parsed = parse.parse(regnum_iu)
    assert len(parsed) == 1
    assert parsed[0]['book'] == '"FROGIKIN" DRAWINGS to show internal structure of frog, by Ada Louise Weckel.'
    assert parsed[0]['oreg'] == 'IU8397'


def test_regnum_j(regnum_j):
    parsed = parse.parse(regnum_j)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'HEAD OF CHRIST IN BAS RELIEF, by W. Clark Noble.'
    assert parsed[0]['oreg'] == 'J259120'


def test_regnum_k(regnum_k):
    parsed = parse.parse(regnum_k)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'AND SO, AS WE SAID BEFORE; by [International Feature Service, inc., as employer for hire of George] Herriman. (In Krazy Kat)'
    assert parsed[0]['oreg'] == 'K167207'


def test_regnum_l(regnum_l):
    parsed = parse.parse(regnum_l)
    assert len(parsed) == 1
    assert parsed[0]['book'] == "ADAM'S RIB, a photoplay in ten reels, by Famous Players-Lasky Corp."
    assert parsed[0]['oreg'] == 'L18658'


def test_regnum_print(regnum_print):
    parsed = parse.parse(regnum_print)
    assert len(parsed) == 1
    assert parsed[0]['book'] == 'BRILLO MAKES OLD ALUMINUM UTENSILS NEW. (Cleaning end polishing outfits)'
    assert parsed[0]['oreg'] == 'Print 6158'
